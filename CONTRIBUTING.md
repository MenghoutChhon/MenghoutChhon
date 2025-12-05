# Contributing to Khmer AI/ML Platform

Thank you for your interest in contributing to the Khmer AI/ML Platform! This document provides guidelines and instructions for contributing.

## 📋 Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Making Changes](#making-changes)
5. [Submitting Changes](#submitting-changes)
6. [Coding Standards](#coding-standards)
7. [Testing Guidelines](#testing-guidelines)

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Respect different viewpoints and experiences

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Git
- Basic understanding of FastAPI and Next.js

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/MenghoutChhon.git
   cd MenghoutChhon
   ```

3. Add upstream remote:
   ```bash
   git remote add upstream https://github.com/MenghoutChhon/MenghoutChhon.git
   ```

## Development Setup

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Setup

```bash
cd frontend
npm install
```

### Run Development Servers

```bash
# Terminal 1 - Backend
cd backend
uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

## Making Changes

### Branch Naming

- Feature: `feature/description`
- Bug fix: `fix/description`
- Documentation: `docs/description`
- Performance: `perf/description`

Example:
```bash
git checkout -b feature/add-khmer-translation
```

### Commit Messages

Follow conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test additions or changes
- `chore:` Build process or auxiliary tool changes

Example:
```
feat: add Khmer language support for OCR

- Implement TrOCR model integration
- Add Khmer character recognition
- Update API endpoint documentation
```

## Submitting Changes

### Pull Request Process

1. **Update your fork**:
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create feature branch**:
   ```bash
   git checkout -b feature/your-feature
   ```

3. **Make changes and commit**:
   ```bash
   git add .
   git commit -m "feat: your feature description"
   ```

4. **Push to your fork**:
   ```bash
   git push origin feature/your-feature
   ```

5. **Create Pull Request**:
   - Go to GitHub
   - Click "New Pull Request"
   - Select your branch
   - Fill out the PR template
   - Submit for review

### PR Requirements

- [ ] Code follows project style guidelines
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] No merge conflicts
- [ ] PR description explains changes

## Coding Standards

### Python (Backend)

#### Style Guide

- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use docstrings for functions and classes

Example:
```python
from typing import Optional

def process_text(
    text: str,
    max_length: Optional[int] = 150
) -> dict:
    """
    Process and summarize text.
    
    Args:
        text: Input text to process
        max_length: Maximum length of output
        
    Returns:
        Dictionary containing processed result
    """
    # Implementation
    return {"result": "processed"}
```

#### Code Organization

```python
# Standard library imports
import os
from typing import List

# Third-party imports
from fastapi import FastAPI
from transformers import AutoModel

# Local imports
from models.tts_model import TTSModel
```

### TypeScript/React (Frontend)

#### Style Guide

- Use TypeScript for type safety
- Use functional components with hooks
- Follow React best practices
- Use Tailwind CSS for styling

Example:
```typescript
'use client'

import { useState } from 'react'

interface TTSProps {
  defaultText?: string
}

export default function TTSComponent({ defaultText = '' }: TTSProps) {
  const [text, setText] = useState<string>(defaultText)
  const [loading, setLoading] = useState<boolean>(false)
  
  const handleSubmit = async () => {
    setLoading(true)
    try {
      // Implementation
    } catch (error) {
      console.error(error)
    } finally {
      setLoading(false)
    }
  }
  
  return (
    <div className="container">
      {/* JSX */}
    </div>
  )
}
```

### File Naming

- Python: `snake_case.py`
- TypeScript/React: `PascalCase.tsx` for components, `camelCase.ts` for utilities
- CSS: `kebab-case.css`

## Testing Guidelines

### Backend Tests

Create tests in `backend/tests/`:

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    
def test_tts_synthesis():
    response = client.post(
        "/api/tts/synthesize",
        json={"text": "test", "language": "khmer"}
    )
    assert response.status_code == 200
```

Run tests:
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests

Create tests in `frontend/__tests__/`:

```typescript
import { render, screen } from '@testing-library/react'
import Home from '@/app/page'

describe('Home', () => {
  it('renders heading', () => {
    render(<Home />)
    expect(screen.getByText(/Khmer AI/i)).toBeInTheDocument()
  })
})
```

Run tests:
```bash
cd frontend
npm test
```

## Documentation

### Code Documentation

- Add docstrings to all functions
- Comment complex logic
- Update README when adding features
- Add examples for new APIs

### API Documentation

FastAPI automatically generates docs. Ensure:

- Endpoint descriptions are clear
- Request/response models are defined
- Examples are provided

```python
@router.post("/synthesize", response_model=TTSResponse)
async def synthesize_speech(request: TTSRequest):
    """
    Convert Khmer text to speech using Meta's MMS-TTS model.
    
    Example request:
    ```json
    {
      "text": "សួស្តី",
      "language": "khmer"
    }
    ```
    """
    # Implementation
```

## Adding New Features

### Checklist for New AI Models

- [ ] Add model handler in `backend/models/`
- [ ] Create API router in `backend/api/`
- [ ] Register router in `backend/main.py`
- [ ] Add frontend page in `frontend/app/`
- [ ] Update model requirements in `requirements.txt`
- [ ] Add model documentation
- [ ] Create tests
- [ ] Update API_TESTING.md

### Example: Adding New Model

1. **Backend Model Handler**:
   ```python
   # backend/models/translation_model.py
   class TranslationModel:
       def __init__(self):
           self.model = None
       
       def translate(self, text: str) -> str:
           # Implementation
           pass
   ```

2. **API Router**:
   ```python
   # backend/api/translation_router.py
   from fastapi import APIRouter
   router = APIRouter()
   
   @router.post("/translate")
   async def translate_text(text: str):
       # Implementation
       pass
   ```

3. **Register Router**:
   ```python
   # backend/main.py
   from api import translation_router
   app.include_router(translation_router.router, prefix="/api/translate")
   ```

## Review Process

1. **Automated Checks**: CI/CD runs tests
2. **Code Review**: Maintainer reviews code
3. **Feedback**: Address review comments
4. **Approval**: Get approval from maintainer
5. **Merge**: Maintainer merges PR

## Getting Help

- **GitHub Issues**: Report bugs or request features
- **Email**: menghoutchhon003@gmail.com
- **Documentation**: Check existing docs first

## Recognition

Contributors will be acknowledged in:
- CONTRIBUTORS.md file
- Release notes
- GitHub contributors page

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to the Khmer AI/ML Platform! 🇰🇭
