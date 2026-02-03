# Fruit Weighting System Interface

A Flask-based web application that provides a user interface for a fruit weighing system. The application connects to a backend service to display real-time information about fruits placed on a weighing scale, including weight, price, and freshness assessment.

## Project Overview

This application serves as the frontend interface for a fruit weighing system that integrates with various backend services including camera feeds, weight sensors, and quality assessment systems. It displays real-time information about fruits including weight, price calculations, and freshness assessments.

## Features

- Real-time display of fruit weight, pricing, and quality assessment
- Live camera feed integration
- Freshness quality visualization with color-coded indicators
- Responsive web interface suitable for use in retail environments
- Staff access modal for administrative functions

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.8 or higher
- Docker and Docker Compose (for containerized deployment)
- Git for version control
- Access to the backend services (uiserver) for full functionality

## Installation

### Option 1: Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
export UI_SERVER_URL=http://localhost:8500
```

5. Run the application:
```bash
python app.py
```

### Option 2: Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Build and start the services:
```bash
docker-compose up --build
```

The application will be available at `http://localhost:5000`.

## Usage

Once the application is running:

1. Navigate to `http://localhost:5000` in your browser
2. The interface will display real-time information from the backend services
3. If backend services are not available, the interface will show "No data" placeholders
4. Click the staff icon (👤) in the bottom right corner to access the staff modal

### Environment Variables

The application uses the following environment variables:

- `UI_SERVER_URL`: Base URL for the backend UI server (default: `http://localhost:8500`)
- `FLASK_ENV`: Flask environment setting (default: `production`)
- `PORT`: Port on which the application runs (default: `5000`)

## Configuration

### Docker Compose Services

The docker-compose.yml file defines the following service:
- `interface`: Main Flask application serving the UI


### Health Checks

Health checks are implemented to ensure service availability:
- Interface service: Checks if the Flask application is responding
- Dependencies: Monitors connection to required backend services

## API Endpoints

The application consumes the following endpoints from the backend service:

- `GET /api/current`: Retrieves current aggregated data about the fruit
- `GET /image/{image_id}`: Fetches camera image by ID

## Troubleshooting

### Common Issues

#### Application fails to start
- Check that all required environment variables are set
- Verify that the UI server is accessible at the configured URL
- Review logs for specific error messages

#### No data displayed
- Confirm that backend services (uiserver) are running
- Verify network connectivity between services
- Check that camera and weight sensor services are operational

#### Docker container fails to build
- Ensure Docker is running and accessible
- Verify that the Dockerfile is correctly formatted
- Check that all required files are present in the build context

### Debugging Tips

- Enable Flask debug mode by setting `FLASK_ENV=development`
- Check application logs: `docker-compose logs interface`
- Verify network connectivity between containers: `docker network ls`

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions, please contact the development team or open an issue in the repository tracker.
