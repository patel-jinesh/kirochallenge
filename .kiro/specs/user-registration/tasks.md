# Implementation Plan

- [ ] 1. Extend data models for user registration system
  - Add User, Registration models to models.py
  - Extend Event model with hasWaitlist and registeredCount fields
  - Add validation for new fields
  - _Requirements: 1.1, 1.2, 1.3, 2.1, 2.2, 2.3, 2.4_

- [ ]* 1.1 Write property test for event initialization invariant
  - **Property 2: Event initialization invariant**
  - **Validates: Requirements 2.4**

- [ ] 2. Update DynamoDB schema and add GSI
  - Modify infrastructure/stacks/backend_stack.py to add GSI1 (GSI1PK, GSI1SK)
  - Update table definition to support single-table design pattern
  - _Requirements: All - infrastructure foundation_

- [ ] 3. Implement user management in database layer
  - Add create_user, get_user, list_users methods to DynamoDBClient
  - Implement PK/SK pattern for user items (PK: USER#{userId}, SK: METADATA)
  - Add duplicate userId detection
  - _Requirements: 1.1, 1.2_

- [ ]* 3.1 Write property test for user creation round trip
  - **Property 1: User creation round trip**
  - **Validates: Requirements 1.1**

- [ ] 4. Implement registration data access methods
  - Add create_registration, get_registration, delete_registration to DynamoDBClient
  - Implement PK/SK pattern for registration items
  - Add GSI1 query methods for user-to-registrations lookup
  - Add methods to query registrations by event (registered and waitlisted separately)
  - _Requirements: 3.1, 4.1, 5.1_

- [ ] 5. Create registration manager business logic
  - Create registration_manager.py with RegistrationManager class
  - Implement register_user method with capacity checking
  - Implement logic to add to waitlist when event is full
  - Implement unregister_user method with waitlist promotion
  - Use DynamoDB transactions for atomic operations
  - _Requirements: 3.1, 3.2, 3.3, 4.1, 4.2_

- [ ]* 5.1 Write property test for registration count increases by one
  - **Property 8: Registration increases count by one**
  - **Validates: Requirements 3.1**

- [ ]* 5.2 Write property test for waitlist ordering preservation
  - **Property 3: Waitlist ordering preservation**
  - **Validates: Requirements 3.3, 6.2**

- [ ]* 5.3 Write property test for registration count consistency
  - **Property 4: Registration count consistency**
  - **Validates: Requirements 6.1**

- [ ] 6. Implement waitlist promotion logic
  - Add promote_from_waitlist method to RegistrationManager
  - Implement atomic transaction to move user from waitlist to registered
  - Update event registeredCount during promotion
  - _Requirements: 4.2_

- [ ]* 6.1 Write property test for waitlist promotion on unregister
  - **Property 5: Waitlist promotion on unregister**
  - **Validates: Requirements 4.2**

- [ ]* 6.2 Write property test for waitlist removal preserves order
  - **Property 6: Waitlist removal preserves order**
  - **Validates: Requirements 4.3**

- [ ]* 6.3 Write property test for unregistration decreases count
  - **Property 9: Unregistration decreases count by one**
  - **Validates: Requirements 4.1**

- [ ] 7. Add user management API endpoints
  - Add POST /users endpoint to create users
  - Add GET /users/{userId} endpoint to get user details
  - Add GET /users endpoint to list all users
  - Add error handling for duplicate userIds and missing fields
  - _Requirements: 1.1, 1.2, 1.3_

- [ ] 8. Add registration API endpoints
  - Add POST /events/{eventId}/register endpoint
  - Add DELETE /events/{eventId}/register/{userId} endpoint
  - Add GET /users/{userId}/registrations endpoint
  - Add GET /events/{eventId}/registrations endpoint
  - Add GET /events/{eventId}/waitlist endpoint
  - Implement proper error responses (404, 409, 422)
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 4.1, 4.4, 5.1, 5.2, 5.3, 5.4_

- [ ]* 8.1 Write property test for user registrations query accuracy
  - **Property 7: User registrations query accuracy**
  - **Validates: Requirements 5.1, 5.2**

- [ ] 9. Update backend requirements.txt
  - Add hypothesis library for property-based testing
  - Add pytest and pytest-asyncio for testing
  - _Requirements: Testing infrastructure_

- [ ] 10. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.
