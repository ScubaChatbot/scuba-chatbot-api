# ScubaTours Chatbot

## USER STORY 1

### Persona: 
Adventure Traveler

### Statement:
**As a** traveler looking for a diving experience  
**I want to** check the availability and details of diving tours in Providencia  
**So I can** plan my vacation.

### Benefit:
Helps me make informed booking decisions.

### Acceptance Criteria:
- I can ask about available tour packages in Providencia.
- The chatbot replies with a list of available dates, prices, and included services.
- If no packages are available, the chatbot informs me politely.

### Mapped Endpoint:
`POST /chat`

---
## USER STORY 2

### Persona: 
Course Seeker

### Statement:
**As a** customer interested in learning to dive  
**I want to** view the upcoming Free Diving courses and their requirements  
**So that** I can choose the one that fits my physical capabilities.

### Benefit:
Allows me to choose a course that fits my skill level and schedule.

### Acceptance Criteria:
  - I can request information about Free Diving courses.
  - The chatbot provides physical requirements, start dates, and price.

### Mapped Endpoint:
`POST /chat`

---
## USER STORY 3

### Persona: 
New Customer

### Statement:
**As a** new user  
**I want to** register and start chatting with the AI  
**So that** I’m able to ask about tours and courses.

### Benefit:
Ensures secure and personalized chatbot interaction.

### Acceptance Criteria:
  - I can register with name, email, and password.
  - I can log in and start a secure chat session.

### Mapped Endpoint:
  `POST /users/register`  
  `POST /users/login`
  `POST /chat`

---
## USER STORY 4

### Persona: 
Curious Customer

### Statement:
**As a** user  
**I want to** ask the chatbot about what’s included in a specific tour to San Andrés  
**So I can** set the budget I need for my vacation.

### Benefit:
Helps me understand if it fits my needs (food, hotel, guided tour).

### Acceptance Criteria:
  - I ask about the San Andrés tour.
  - The chatbot lists the services included in available tour packages.

### Mapped Endpoint:
  `POST /chat`

---

## USER STORY 5

### Persona: 
Returning Customer

### Statement:
**As a** returning client  
**I want to** check the status of my diving tour booking  
**So I can** confirm if it’s active.

### Benefit:
Provides peace of mind and clarity before travel.

### Acceptance Criteria:
  - I can enter my booking ID.
  - The chatbot confirms my booking status (confirmed, pending, or cancelled) and shows details.

### Mapped Endpoint:  
  `POST /chat`