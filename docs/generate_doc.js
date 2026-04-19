const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  HeadingLevel, AlignmentType, BorderStyle, WidthType, ShadingType,
  LevelFormat, PageBreak
} = require("docx");
const fs = require("fs");

const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };

const h1 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_1,
  children: [new TextRun({ text, bold: true, color: "1a1a2e", size: 32, font: "Arial" })],
  spacing: { before: 400, after: 200 }
});

const h2 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_2,
  children: [new TextRun({ text, bold: true, color: "e94560", size: 26, font: "Arial" })],
  spacing: { before: 300, after: 160 }
});

const h3 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_3,
  children: [new TextRun({ text, bold: true, color: "0f3460", size: 24, font: "Arial" })],
  spacing: { before: 200, after: 120 }
});

const para = (text) => new Paragraph({
  children: [new TextRun({ text, size: 22, font: "Arial" })],
  spacing: { before: 120, after: 120 },
  alignment: AlignmentType.JUSTIFIED
});

const bullet = (text) => new Paragraph({
  numbering: { reference: "bullets", level: 0 },
  children: [new TextRun({ text, size: 22, font: "Arial" })],
  spacing: { before: 60, after: 60 }
});

const numbered = (text) => new Paragraph({
  numbering: { reference: "numbers", level: 0 },
  children: [new TextRun({ text, size: 22, font: "Arial" })],
  spacing: { before: 60, after: 60 }
});

const tableRow = (cells, isHeader = false) => new TableRow({
  children: cells.map(cell => new TableCell({
    borders,
    width: { size: Math.floor(9360 / cells.length), type: WidthType.DXA },
    shading: isHeader ? { fill: "1a1a2e", type: ShadingType.CLEAR } : { fill: "FFFFFF", type: ShadingType.CLEAR },
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    children: [new Paragraph({
      alignment: isHeader ? AlignmentType.CENTER : AlignmentType.LEFT,
      children: [new TextRun({ text: cell, bold: isHeader, color: isHeader ? "FFFFFF" : "333333", size: 20, font: "Arial" })]
    })]
  }))
});

const makeTable = (headers, rows) => new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: headers.map(() => Math.floor(9360 / headers.length)),
  rows: [tableRow(headers, true), ...rows.map(r => tableRow(r))]
});

const pageBreak = () => new Paragraph({ children: [new PageBreak()] });

const doc = new Document({
  numbering: {
    config: [
      { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "numbers", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] }
    ]
  },
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 32, bold: true, font: "Arial" }, paragraph: { spacing: { before: 400, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 26, bold: true, font: "Arial" }, paragraph: { spacing: { before: 300, after: 160 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 24, bold: true, font: "Arial" }, paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 } }
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1080, bottom: 1440, left: 1080 }
      }
    },
    children: [
      // ─── Title Page ───────────────────────────────────────────────────────
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 1440, after: 400 },
        children: [new TextRun({ text: "G. PULLA REDDY ENGINEERING COLLEGE", bold: true, size: 36, font: "Arial", color: "1a1a2e" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 0, after: 200 },
        children: [new TextRun({ text: "(Autonomous), Kurnool", size: 26, font: "Arial", color: "555555" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 0, after: 600 },
        children: [new TextRun({ text: "Department of Computer Science and Engineering", size: 24, font: "Arial", italics: true, color: "555555" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 0, after: 300 },
        children: [new TextRun({ text: "PROJECT DOCUMENTATION", bold: true, size: 40, font: "Arial", color: "e94560", allCaps: true })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "e94560", space: 1 } },
        spacing: { before: 0, after: 600 },
        children: [new TextRun({ text: "GPREC IntelliBot", bold: true, size: 52, font: "Arial", color: "1a1a2e" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 0, after: 800 },
        children: [new TextRun({ text: "An AI-Powered Navigator and Information Hub for Students", size: 28, font: "Arial", italics: true, color: "0f3460" })]
      }),
      makeTable(
        ["S.No", "Roll Number", "Student Name"],
        [["1", "229X1A05E1", "G. Sindhuja"], ["2", "239X5A05M0", "R. Anjali Devi"], ["3", "229X1A0567", "A. Sucharitha Devi"]]
      ),
      new Paragraph({ spacing: { before: 300, after: 160 }, children: [new TextRun({ text: "Guide: D.L.N Prasunna, Assistant Professor", size: 22, bold: true, font: "Arial" })] }),
      new Paragraph({ spacing: { before: 0, after: 160 }, children: [new TextRun({ text: "Batch No: CSE-A7  |  Date: 14/7/2025", size: 22, font: "Arial", color: "666666" })] }),

      pageBreak(),

      // ─── 1. Introduction ──────────────────────────────────────────────────
      h1("1. Introduction"),
      para("Transitioning into college life can be a challenging experience for new students. They often struggle to access essential information related to campus navigation, administrative procedures, academic schedules, and placement processes. To bridge this significant gap, we present GPREC IntelliBot - an intelligent, multilingual AI-powered student assistant specifically designed for G. Pulla Reddy Engineering College (GPREC), Kurnool."),
      para("GPREC IntelliBot leverages state-of-the-art machine learning and natural language processing (NLP) technology, powered by Google's Gemini 1.5 Flash model, to deliver personalized, real-time guidance and support to students at all stages of their engineering education journey. The system goes beyond traditional static rule-based bots by integrating core ML components to enhance user interaction and adaptability."),

      h2("1.1 Problem Statement"),
      para("Students at GPREC face several challenges that this project addresses:"),
      bullet("Difficulty navigating a large campus with multiple departments and facilities"),
      bullet("Lack of easy access to placement eligibility information and company requirements"),
      bullet("Delayed access to important notifications about exams, events, and placements"),
      bullet("Language barriers for students who prefer regional languages (Telugu, Hindi)"),
      bullet("Dependency on senior students or staff for basic information queries"),

      h2("1.2 Objectives"),
      numbered("Develop an AI-powered chatbot capable of understanding natural language queries from students"),
      numbered("Implement an interactive campus map for visual navigation assistance"),
      numbered("Build a placement analyzer that matches student profiles to eligible companies"),
      numbered("Create a real-time notification system for campus updates"),
      numbered("Support multiple languages including English, Telugu, and Hindi"),
      numbered("Provide a clean, modern, and intuitive user interface accessible on any device"),

      pageBreak(),

      // ─── 2. Technology Stack ──────────────────────────────────────────────
      h1("2. Technology Stack"),
      para("GPREC IntelliBot is built using a modern, scalable technology stack that ensures high performance, maintainability, and ease of deployment."),

      makeTable(
        ["Layer", "Technology", "Version", "Purpose"],
        [
          ["Frontend", "Streamlit", "1.39.0", "Interactive web UI framework"],
          ["Backend", "FastAPI", "0.115.0", "High-performance REST API server"],
          ["Runtime", "Python", "3.10+", "Primary programming language"],
          ["AI Engine", "Google Gemini", "1.5 Flash", "Natural language processing & generation"],
          ["Database", "SQLite + SQLAlchemy", "2.0.35", "Persistent data storage"],
          ["AI SDK", "google-generativeai", "0.8.3", "Gemini API integration"],
          ["ASGI Server", "Uvicorn", "0.30.6", "Production-grade server"],
          ["Testing", "Pytest", "Latest", "Unit and integration testing"],
          ["OS", "Windows 10/11", "-", "Target deployment platform"],
        ]
      ),

      h2("2.1 Why This Stack?"),
      bullet("FastAPI: Automatically generates API documentation, supports async operations, and has excellent performance benchmarks"),
      bullet("Streamlit: Enables rapid development of data-driven web applications with pure Python - no HTML/CSS/JS expertise required"),
      bullet("Google Gemini: State-of-the-art multilingual AI model with strong reasoning capabilities and fast response times"),
      bullet("SQLite: Lightweight, serverless database perfect for a campus deployment without infrastructure overhead"),
      bullet("SQLAlchemy: Industry-standard ORM providing database abstraction and easy migrations"),

      pageBreak(),

      // ─── 3. System Architecture ───────────────────────────────────────────
      h1("3. System Architecture"),
      para("GPREC IntelliBot follows a clean, layered architecture that separates concerns and ensures maintainability. The system consists of three primary layers: the presentation layer (Streamlit frontend), the business logic layer (FastAPI backend), and the data layer (SQLite database + Gemini AI)."),

      h2("3.1 Architecture Overview"),
      para("The application follows a client-server architecture with the following communication flow:"),
      numbered("Student opens the Streamlit frontend in their browser (localhost:8501)"),
      numbered("User actions (chat messages, profile submissions) are sent as HTTP requests to the FastAPI backend (localhost:8000)"),
      numbered("FastAPI processes the request, queries the database if needed, and calls the Gemini AI API"),
      numbered("Gemini AI returns a contextually relevant response based on the GPREC-specific system prompt"),
      numbered("FastAPI returns the formatted response to the Streamlit frontend"),
      numbered("Streamlit renders the response in the chat interface with proper formatting"),

      h2("3.2 Project Structure"),
      makeTable(
        ["Directory/File", "Description"],
        [
          ["backend/main.py", "FastAPI application entry point with middleware setup"],
          ["backend/config.py", "Configuration, Gemini API key, campus data, company data"],
          ["backend/database.py", "SQLAlchemy models, database initialization, seeding"],
          ["backend/gemini_service.py", "Google Gemini AI integration service"],
          ["backend/routers/chat.py", "Chat endpoints with conversation history"],
          ["backend/routers/placement.py", "Placement analysis endpoints"],
          ["backend/routers/notifications.py", "Notification CRUD endpoints"],
          ["backend/routers/campus.py", "Campus map and location endpoints"],
          ["frontend/app.py", "Main Streamlit application with all UI pages"],
          ["tests/test_intellibot.py", "Comprehensive test suite (40+ test cases)"],
          ["requirements.txt", "Python dependency list"],
          ["START_APP.bat", "One-click Windows launcher"],
          ["start_backend.bat", "Backend-only Windows launcher"],
          ["start_frontend.bat", "Frontend-only Windows launcher"],
        ]
      ),

      pageBreak(),

      // ─── 4. Features ──────────────────────────────────────────────────────
      h1("4. Features and Functionality"),

      h2("4.1 NLP-Based Chat (IntelliBot Chat)"),
      para("The core feature of GPREC IntelliBot is its AI-powered conversational interface. The chatbot uses Google Gemini 1.5 Flash to understand and respond to diverse student queries with context-awareness and personalization."),
      bullet("Maintains conversation history within a session for contextual responses"),
      bullet("Understands queries in English, Telugu, and Hindi"),
      bullet("Responds with specific GPREC information including locations, timings, contacts"),
      bullet("Quick question buttons in sidebar for common queries"),
      bullet("Session management allowing students to start fresh conversations"),

      h2("4.2 Interactive Campus Map"),
      para("The campus map page provides a visual, SVG-based representation of the GPREC campus with 15+ marked locations."),
      bullet("Color-coded location markers by category (Admin, Department, Facility, Hostel, Sports)"),
      bullet("Click-to-select any location for detailed information"),
      bullet("AI-powered direction service between any two campus locations"),
      bullet("Search functionality to find specific locations by name or description"),
      bullet("Comprehensive legend explaining all location categories"),

      h2("4.3 Placement Analyzer & Predictor"),
      para("This feature helps students understand their placement eligibility and receive personalized career guidance."),
      bullet("Input student profile: branch, CGPA, year, skills, backlogs"),
      bullet("Automatic matching against 15+ companies with eligibility criteria"),
      bullet("AI-generated personalized advice including top 3 company recommendations"),
      bullet("Skills gap analysis with specific improvement suggestions"),
      bullet("Placement statistics dashboard with historical data"),

      h2("4.4 Real-Time Notification System"),
      para("The notification system keeps students informed about campus activities and important deadlines."),
      bullet("Category-based filtering: Placement drives, Examinations, Events, General announcements"),
      bullet("Branch-specific notifications (e.g., CSE-only placement drives)"),
      bullet("Color-coded notification cards for quick visual identification"),
      bullet("Pre-seeded with 5 sample notifications on first startup"),
      bullet("Admin API endpoint for creating new notifications"),

      h2("4.5 College Information Hub"),
      para("A comprehensive information page about GPREC with quick facts, contact details, and department information readily accessible without requiring any AI queries."),

      pageBreak(),

      // ─── 5. API Documentation ─────────────────────────────────────────────
      h1("5. API Documentation"),
      para("The FastAPI backend automatically generates interactive API documentation accessible at http://localhost:8000/docs when the server is running."),

      h2("5.1 Chat Endpoints"),
      makeTable(
        ["Method", "Endpoint", "Description", "Auth"],
        [
          ["POST", "/api/chat/message", "Send a message and get AI response", "None"],
          ["GET", "/api/chat/history/{session_id}", "Retrieve conversation history", "None"],
          ["POST", "/api/chat/navigate", "Get campus navigation directions", "None"],
          ["DELETE", "/api/chat/session/{session_id}", "Clear a chat session", "None"],
        ]
      ),

      h2("5.2 Placement Endpoints"),
      makeTable(
        ["Method", "Endpoint", "Description", "Auth"],
        [
          ["POST", "/api/placement/analyze", "Analyze student profile for placement", "None"],
          ["GET", "/api/placement/companies", "Get all placement companies", "None"],
          ["GET", "/api/placement/companies/filter", "Filter by branch and CGPA", "None"],
          ["GET", "/api/placement/stats", "Get placement statistics", "None"],
        ]
      ),

      h2("5.3 Campus Endpoints"),
      makeTable(
        ["Method", "Endpoint", "Description", "Auth"],
        [
          ["GET", "/api/campus/locations", "Get all campus locations", "None"],
          ["GET", "/api/campus/locations/{id}", "Get specific location", "None"],
          ["GET", "/api/campus/search?query=X", "Search locations", "None"],
          ["GET", "/api/campus/college-info", "Get college information", "None"],
        ]
      ),

      h2("5.4 Notification Endpoints"),
      makeTable(
        ["Method", "Endpoint", "Description", "Auth"],
        [
          ["GET", "/api/notifications/", "Get all notifications (with filters)", "None"],
          ["POST", "/api/notifications/", "Create a new notification", "Admin"],
          ["GET", "/api/notifications/categories", "Get available categories", "None"],
        ]
      ),

      pageBreak(),

      // ─── 6. Installation ──────────────────────────────────────────────────
      h1("6. Installation and Setup (Windows)"),

      h2("6.1 Prerequisites"),
      bullet("Windows 10 or Windows 11 (64-bit)"),
      bullet("Python 3.10 or higher (download from https://python.org)"),
      bullet("Internet connection (for Gemini API calls)"),
      bullet("Minimum 4GB RAM recommended"),

      h2("6.2 Quick Start (Recommended)"),
      numbered("Download/extract the project folder to any location (e.g., C:\\GPREC_IntelliBot\\)"),
      numbered("Double-click START_APP.bat - this installs all dependencies automatically"),
      numbered("Wait for both servers to start (approximately 15-30 seconds)"),
      numbered("The browser will automatically open at http://localhost:8501"),
      numbered("Start chatting with GPREC IntelliBot!"),

      h2("6.3 Manual Setup"),
      new Paragraph({
        children: [new TextRun({ text: "Step 1: Install Dependencies", bold: true, size: 22, font: "Arial" })],
        spacing: { before: 160, after: 80 }
      }),
      new Paragraph({
        children: [new TextRun({ text: "pip install -r requirements.txt", size: 20, font: "Courier New", color: "0f3460" })],
        spacing: { before: 60, after: 120 },
        indent: { left: 720 }
      }),
      new Paragraph({
        children: [new TextRun({ text: "Step 2: Start Backend (Terminal 1)", bold: true, size: 22, font: "Arial" })],
        spacing: { before: 160, after: 80 }
      }),
      new Paragraph({
        children: [new TextRun({ text: "cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload", size: 20, font: "Courier New", color: "0f3460" })],
        spacing: { before: 60, after: 120 },
        indent: { left: 720 }
      }),
      new Paragraph({
        children: [new TextRun({ text: "Step 3: Start Frontend (Terminal 2)", bold: true, size: 22, font: "Arial" })],
        spacing: { before: 160, after: 80 }
      }),
      new Paragraph({
        children: [new TextRun({ text: "cd frontend && streamlit run app.py --server.port 8501", size: 20, font: "Courier New", color: "0f3460" })],
        spacing: { before: 60, after: 120 },
        indent: { left: 720 }
      }),
      new Paragraph({
        children: [new TextRun({ text: "Step 4: Run Tests (Optional)", bold: true, size: 22, font: "Arial" })],
        spacing: { before: 160, after: 80 }
      }),
      new Paragraph({
        children: [new TextRun({ text: "pytest tests/ -v", size: 20, font: "Courier New", color: "0f3460" })],
        spacing: { before: 60, after: 120 },
        indent: { left: 720 }
      }),

      h2("6.4 Access Points"),
      makeTable(
        ["Service", "URL", "Description"],
        [
          ["Frontend", "http://localhost:8501", "Main Streamlit application"],
          ["Backend API", "http://localhost:8000", "FastAPI server"],
          ["API Docs", "http://localhost:8000/docs", "Interactive Swagger documentation"],
          ["API Alt Docs", "http://localhost:8000/redoc", "ReDoc API documentation"],
        ]
      ),

      pageBreak(),

      // ─── 7. Testing ───────────────────────────────────────────────────────
      h1("7. Testing"),
      para("GPREC IntelliBot includes a comprehensive test suite with 40+ test cases covering all major features and edge cases. Tests are written using pytest and use mock objects to simulate Gemini API calls for reliable, fast execution."),

      h2("7.1 Test Categories"),
      makeTable(
        ["Test Class", "Tests", "Description"],
        [
          ["TestHealthEndpoints", "4", "API health and root endpoint checks"],
          ["TestChatAPI", "10", "Chat messaging, history, navigation"],
          ["TestCampusAPI", "9", "Location data, search, navigation"],
          ["TestPlacementAPI", "9", "Company filtering, analysis, statistics"],
          ["TestNotificationsAPI", "6", "CRUD operations, filtering"],
          ["TestConfigAndData", "6", "Data integrity and configuration validation"],
          ["TestEdgeCases", "5", "Boundary conditions and error handling"],
        ]
      ),

      h2("7.2 Running Tests"),
      new Paragraph({
        children: [new TextRun({ text: "# Run all tests\npytest tests/ -v\n\n# Run specific test class\npytest tests/ -v -k TestChatAPI\n\n# Run with coverage report\npytest tests/ -v --tb=short", size: 20, font: "Courier New", color: "0f3460" })],
        spacing: { before: 60, after: 120 },
        indent: { left: 720 }
      }),

      h2("7.3 Sample Test Output"),
      para("Expected output when all tests pass:"),
      new Paragraph({
        children: [new TextRun({ text: "====== 40 passed in X.XXs ======", size: 20, font: "Courier New", color: "27ae60" })],
        spacing: { before: 60, after: 120 },
        indent: { left: 720 }
      }),

      pageBreak(),

      // ─── 8. Future Enhancements ───────────────────────────────────────────
      h1("8. Future Enhancements"),
      para("The current implementation provides a solid foundation. The following enhancements are planned for future iterations:"),

      h2("8.1 Technical Enhancements"),
      bullet("Voice interaction support using Web Speech API and Google Text-to-Speech for hands-free operation"),
      bullet("Mobile application using React Native or Flutter for Android/iOS"),
      bullet("Integration with official GPREC student portal for real exam schedules and results"),
      bullet("PostgreSQL migration for multi-server production deployment"),
      bullet("Redis caching for improved response times"),
      bullet("User authentication with student roll number and password"),

      h2("8.2 Feature Enhancements"),
      bullet("Real-time placement drive registration through the chatbot interface"),
      bullet("Study material recommendation based on current exam schedules"),
      bullet("Alumni connection feature for mentorship and career guidance"),
      bullet("Attendance tracking integration with JNTUA systems"),
      bullet("Event registration and management through the notification system"),
      bullet("Image-based queries using Gemini Vision API"),

      h2("8.3 AI Improvements"),
      bullet("Fine-tuning on GPREC-specific FAQ dataset for more accurate responses"),
      bullet("Sentiment analysis to detect student stress and provide mental health resources"),
      bullet("Personalized learning path recommendations based on CGPA trends"),
      bullet("Automated notification generation from college website using web scraping"),

      pageBreak(),

      // ─── 9. Conclusion ────────────────────────────────────────────────────
      h1("9. Conclusion"),
      para("GPREC IntelliBot successfully addresses the core challenge of information accessibility for students at G. Pulla Reddy Engineering College. By combining the power of Google's Gemini AI with a clean, intuitive Streamlit interface and a robust FastAPI backend, we have created a comprehensive digital assistant that can significantly reduce the information gap experienced by students."),
      para("The system's multilingual support makes it accessible to students from diverse linguistic backgrounds, while the placement analyzer provides actionable career guidance that was previously only available through manual counseling sessions. The interactive campus map solves the practical problem of navigation for new students joining the campus."),
      para("This project demonstrates the practical application of modern AI and web technologies in an educational context, showcasing how AI can be used responsibly to enhance the student experience without replacing the human elements of education. The codebase follows best practices with comprehensive testing, clean architecture, and thorough documentation, making it maintainable and extensible for future teams."),

      h2("9.1 Team Contributions"),
      makeTable(
        ["Student Name", "Roll Number", "Contribution"],
        [
          ["G. Sindhuja", "229X1A05E1", "AI/ML Integration, Gemini API, NLP-based chat system"],
          ["R. Anjali Devi", "239X5A05M0", "Frontend (Streamlit UI), Campus Map, Notification System"],
          ["A. Sucharitha Devi", "229X1A0567", "Backend (FastAPI), Database Design, Placement Analyzer"],
        ]
      ),

      new Paragraph({ spacing: { before: 400 }, border: { top: { style: BorderStyle.SINGLE, size: 4, color: "e94560", space: 1 } }, children: [] }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 200, after: 100 },
        children: [new TextRun({ text: "G. Pulla Reddy Engineering College (Autonomous), Kurnool | Batch CSE-A7 | 2025", size: 18, font: "Arial", color: "888888", italics: true })]
      }),
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("GPREC_IntelliBot_Documentation.docx", buffer);
  console.log("Documentation created: GPREC_IntelliBot_Documentation.docx");
});
