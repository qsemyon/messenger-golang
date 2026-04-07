package main

import (
	"database/sql"
	"fmt"
	"log"
	"net/http"
	"os"
	"sync"
	"time"

	"github.com/gorilla/websocket"
	_ "github.com/lib/pq"
)

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool { return true },
}

type Server struct {
	db      *sql.DB
	clients map[*websocket.Conn]bool
	mu      sync.Mutex
}

func main() {
	dbURL := os.Getenv("DB_URL")
	if dbURL == "" {
		dbURL = "postgres://user:password@localhost:5432/vibechat?sslmode=disable"
	}

	var db *sql.DB
	var err error

	for i := 0; i < 5; i++ {
		db, err = sql.Open("postgres", dbURL)
		if err == nil {
			err = db.Ping()
		}
		if err == nil {
			break
		}
		fmt.Printf("Ожидаю базу... попытка %d\n", i+1)
		time.Sleep(2 * time.Second)
	}

	if err != nil {
		log.Fatal("Не удалось подключиться к БД:", err)
	}

	_, err = db.Exec(`CREATE TABLE IF NOT EXISTS messages (
		id SERIAL PRIMARY KEY,
		content TEXT NOT NULL,
		created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	)`)
	if err != nil {
		log.Fatal(err)
	}

	srv := &Server{
		db:      db,
		clients: make(map[*websocket.Conn]bool),
	}

	http.HandleFunc("/ws", srv.handleWS)

	fmt.Println("Сервер чата запущен на :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

func (s *Server) handleWS(w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		return
	}
	defer conn.Close()

	s.mu.Lock()
	s.clients[conn] = true
	s.mu.Unlock()

	s.sendHistory(conn)

	// Внутри цикла for в функции handleWS
	for {
		var msg map[string]string
		// Теперь сообщение от Python прилетает в виде {"content": "...", "sender_id": "..."}
		if err := conn.ReadJSON(&msg); err != nil {
			s.mu.Lock()
			delete(s.clients, conn)
			s.mu.Unlock()
			break
		}

		// Сохраняем в базу (только контент, ID сессии нам там не нужен)
		_, err := s.db.Exec("INSERT INTO messages (content) VALUES ($1)", msg["content"])
		if err != nil {
			fmt.Println("DB Error:", err)
		}

		// Рассылаем ВСЕМ сообщение целиком (вместе с sender_id)
		s.broadcast(msg)
	}
}

func (s *Server) sendHistory(conn *websocket.Conn) {
	rows, err := s.db.Query("SELECT content FROM messages ORDER BY id ASC LIMIT 100")
	if err != nil {
		return
	}
	defer rows.Close()

	for rows.Next() {
		var content string
		if err := rows.Scan(&content); err == nil {
			conn.WriteJSON(map[string]string{"content": content})
		}
	}
}

func (s *Server) broadcast(msg map[string]string) {
	s.mu.Lock()
	defer s.mu.Unlock()
	for client := range s.clients {
		err := client.WriteJSON(msg)
		if err != nil {
			client.Close()
			delete(s.clients, client)
		}
	}
}
