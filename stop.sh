#!/bin/bash

# Khmer AI/ML Platform - Stop Script

set -e

echo "🛑 Stopping Khmer AI/ML Platform..."

# Stop and remove containers
docker-compose down

echo "✅ Services stopped successfully!"
echo ""
echo "To remove volumes as well, run:"
echo "   docker-compose down -v"
