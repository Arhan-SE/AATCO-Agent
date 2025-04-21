# AATCO Email Automation - Multi-Agent System Architecture

## Overview
This document outlines the architecture of a multi-agent system designed to automate AATCO's email communication process for their tool sales business.

## Process Flow

### 1. Initial Inquiry Phase
- Customer submits product requests
- System sends auto-reply acknowledgment
- Response: "Well noted and thanks for the enquiry. Soon you will be updated with the quote."

### 2. Quotation Phase
- Technical Datasheet (TDS) sharing
- Quote provision to customer
- Quote-related discussions

### 3. Payment & Logistics Phase
- Banking details collection
- Proforma invoice generation
- Order confirmation
- Final invoice generation
- Delivery scheduling
- Payment discussions

## Agent Hierarchy

### 1. Master Coordinator Agent
- **Responsibilities:**
  - Oversees entire communication process
  - Routes emails to appropriate specialized agents
  - Maintains conversation state
  - Manages handoffs between phases
  - Ensures process continuity

### 2. Inquiry Processing Agent
- **Responsibilities:**
  - Processes initial customer inquiries
  - Extracts product requirements
  - Generates acknowledgment responses
  - Validates inquiry completeness
  - Identifies required products from catalog

### 3. Quotation Agent
- **Responsibilities:**
  - Processes TDS requests
  - Generates quotes based on product requirements
  - Handles quote-related questions
  - Manages quote revisions
  - Coordinates with pricing database

### 4. Payment & Logistics Agent
- **Responsibilities:**
  - Collects and verifies banking details
  - Generates proforma invoices
  - Processes order confirmations
  - Coordinates delivery scheduling
  - Handles payment-related discussions
  - Generates final invoices
  - Manages payment tracking

### 5. Document Management Agent
- **Responsibilities:**
  - Manages all document attachments
  - Ensures proper document formatting
  - Maintains document versioning
  - Handles document storage and retrieval
  - Manages templates for various documents

### 6. Customer Context Agent
- **Responsibilities:**
  - Maintains customer history
  - Tracks previous interactions
  - Stores customer preferences
  - Provides context to other agents
  - Manages customer relationship data

## System Features

### 1. State Management
- Conversation state tracking
- Context maintenance across emails
- Multi-threaded conversation handling
- Process phase tracking

### 2. Document Processing
- PDF handling (TDS, invoices)
- Document generation
- Attachment management
- Template management

### 3. Natural Language Understanding
- Email content parsing
- Intent recognition
- Entity extraction
- Sentiment analysis

### 4. Response Generation
- Template-based responses
- Dynamic content insertion
- Professional tone maintenance
- Context-aware responses

## Communication Flow
```
Customer Email → Master Coordinator → Specialized Agent → Response → Customer
```

## Technical Requirements
- Python-based implementation
- Email trigger system (existing .py file in trigger folder)
- Database integration for:
  - Customer information
  - Product catalog
  - Pricing information
  - Document templates
  - Conversation history

## Next Steps
1. Implement core agent framework
2. Develop individual agent modules
3. Create communication protocols
4. Implement state management system
5. Develop document processing capabilities
6. Create testing framework
7. Deploy and monitor system 