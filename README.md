# 🧊 Fridgie - Docker Starter Repository

A complete Docker-based starter repository featuring:
- **Python/Flask Backend** - RESTful API with full CRUD operations
- **MySQL Database** - Persistent data storage with sample data
- **Next.js Frontend** - Modern React framework with TypeScript and Tailwind CSS

## 📋 Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 2.0 or higher)

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fridgie
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` if you want to customize the database credentials.

3. **Start all services**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - MySQL: localhost:3306

## 🏗️ Project Structure

```
fridgie/
├── backend/              # Python/Flask backend
│   ├── Dockerfile       # Backend container configuration
│   ├── app.py           # Main Flask application
│   ├── requirements.txt # Python dependencies
│   └── init.sql         # Database initialization script
├── frontend/            # Next.js frontend
│   ├── Dockerfile       # Frontend container configuration
│   ├── app/             # Next.js app directory
│   └── package.json     # Node.js dependencies
├── docker-compose.yml   # Docker Compose configuration
├── .env.example         # Environment variables template
└── README.md           # This file
```

## 🔌 API Endpoints

### Health Check
- `GET /health` - Check API and database connectivity

### Items CRUD
- `GET /api/items` - Get all items
- `POST /api/items` - Create a new item
  ```json
  {
    "name": "Item name",
    "quantity": 1
  }
  ```
- `GET /api/items/:id` - Get a specific item
- `PUT /api/items/:id` - Update an item
- `DELETE /api/items/:id` - Delete an item

## 🛠️ Development

### Starting the services
```bash
docker-compose up
```

### Rebuilding after changes
```bash
docker-compose up --build
```

### Stopping the services
```bash
docker-compose down
```

### Removing all data (including database)
```bash
docker-compose down -v
```

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

## 🗄️ Database

The MySQL database is automatically initialized with a sample schema and data:
- Database name: `fridgie`
- Table: `items` (id, name, quantity, created_at, updated_at)
- Sample data: 5 food items

Database data persists in a Docker volume named `mysql-data`.

## 🎨 Frontend Features

- Modern, responsive UI built with Next.js and Tailwind CSS
- Real-time API connection status indicator
- Add, view, and delete items
- Dark mode support
- TypeScript for type safety

## 🐍 Backend Features

- RESTful API built with Flask
- MySQL database integration
- CORS enabled for frontend connectivity
- Health check endpoint
- Error handling and validation
- Automatic database connection retry

## 🔧 Customization

### Changing Port Numbers

Edit `docker-compose.yml`:
```yaml
services:
  frontend:
    ports:
      - "3000:3000"  # Change first number
  backend:
    ports:
      - "5000:5000"  # Change first number
  db:
    ports:
      - "3306:3306"  # Change first number
```

### Adding New API Endpoints

1. Add new route in `backend/app.py`
2. Test with curl or Postman
3. Update frontend to use the new endpoint

### Modifying Database Schema

1. Edit `backend/init.sql`
2. Remove existing volume: `docker-compose down -v`
3. Rebuild: `docker-compose up --build`

## 🐛 Troubleshooting

### Backend can't connect to database
- Wait a few seconds for MySQL to fully initialize
- Check logs: `docker-compose logs db`
- Verify credentials in `.env` file

### Frontend can't connect to backend
- Ensure backend is running: `docker-compose ps`
- Check `NEXT_PUBLIC_API_URL` in docker-compose.yml
- Verify CORS is enabled in backend

### Port already in use
- Stop conflicting services or change ports in docker-compose.yml
- Use: `lsof -i :3000` (or :5000, :3306) to find conflicting processes

## 📝 License

MIT License - feel free to use this starter template for your projects!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.