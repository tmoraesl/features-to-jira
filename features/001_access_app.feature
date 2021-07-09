Feature: Access Living App
   Scenario: Access App with remote control in decoder
      Tags: uat, regression, desco
      Given: living apps screen is opened
      When: App living app is selected
      Then: initial screen of the living app is displayed
      !image_initial_screen.png|thumbnail!

   Scenario: Access App with Aura in decoder
      Tags: uat, regression, desco, mandovocal
      Given: living apps screen is opened
      When: user says "Abrir App"
      Then: initial screen of the living app is displayed
      And: aura feedback is reproduced with "Bienvenido a la Living App de Experiencias App."
      !image_initial_screen.png|thumbnail!

   Scenario: Access App with Aura in Movistar Home
      Tags: uat, regression, movistarhome
      Given: living apps screen is opened
      When: user says "OK Aura, abrir App"
      Then: initial screen of the living app is displayed
      And: aura feedback is reproduced with "Bienvenido a la Living App de Experiencias App."
      !image_initial_screen.png|thumbnail!

