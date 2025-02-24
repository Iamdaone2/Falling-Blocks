
import pygame
import sys
import random
import time
import math

running = True

game_over = False
# Flag to indicate whether the bot is active
bot_active = False
current_score = 0
high_score = 0
# Pause flag
paused = False
# Initialize Pygame
pygame.init()

blue_bullets = []
SHOOT_COOLDOWN = 125  # Adjust the cooldown duration (in frames)
last_shot_time = 0

blue_objects = []


# Constants
GUN_WIDTH, GUN_HEIGHT = 10, 20

# Constants
WIDTH, HEIGHT = 500, 400
PLAYER_SIZE = 20
FPS = 60

font = pygame.font.Font(None, 30)

# Create the gun
gun = pygame.Rect(WIDTH // 2 - GUN_WIDTH // 2, HEIGHT - GUN_HEIGHT - 30, GUN_WIDTH, GUN_HEIGHT)

# Difficulty levels
difficulty_levels = [
    {"falling_speed": 3},
    {"falling_speed": 5},
    {"falling_speed": 7},
    {"falling_speed": 9},
    {"falling_speed": 12},
    {"falling_speed": 17},
    {"falling_speed": 8, "invisible_delay": 60}
]



# Set the initial difficulty level
current_level = 0

# Set up the player's bullet properties
bullet_width, bullet_height = 8, 10
bullet_speed = 8
bullets = []

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Variable to control game over message display
show_game_over_message = False

# Create the player
# Add gun dimensions to the player rectangle
player = pygame.Rect(WIDTH // 2 - PLAYER_SIZE // 2, HEIGHT - PLAYER_SIZE * 2, PLAYER_SIZE, PLAYER_SIZE)

# Create a list to store falling objects
falling_objects = []

# Set up the Pygame window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Falling Objects")

# Set up the clock to control the frame rate
clock = pygame.time.Clock()

class FallingObject:
  def __init__(self, x, y, width, height, color):
      self.rect = pygame.Rect(x, y, width, height)
      self.color = color

  def move_ip(self, x, y):
      self.rect.x += x
      self.rect.y += y
# Create a list to store falling objects
falling_objects = []

# Function to display the starting screen
def start_screen():
    window.fill((0, 0, 0))

    title_font = pygame.font.Font(None, 50)
    title_text = title_font.render("Dodge the Falling Objects", True, (255, 255, 255))
    window.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

    instructions_text = font.render("Use Arrow Keys to Move Left/Right, Space to Shoot", True, (255, 255, 255))
    instructions_texts = font.render("And 1 to become a dumb silly bot", True, (255, 255, 255))
    instruction_text = font.render("(Not recommended for higher levels)", True, (255, 255, 255))
    instruction_texts = font.render("Hostiles are hidden until halfway in level 7", True, (255, 255, 255))
    window.blit(instructions_text, (WIDTH // 2 - instructions_text.get_width() // 2, 150))
    window.blit(instructions_texts, (WIDTH // 2 - instructions_text.get_width() // 2, 200))
    window.blit(instruction_text, (WIDTH // 2 - instructions_text.get_width() // 2, 250))
    window.blit(instruction_texts, (WIDTH // 2 - instructions_text.get_width() // 2, 300))

    start_text = font.render("Press Enter to Start", True, (255, 255, 255))
    window.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT - 50))

    pygame.display.flip()

start_screen()

# Wait for Enter key press to start the game
waiting_for_start = True
while waiting_for_start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            waiting_for_start = False

    # Display the starting screen
    start_screen()

# Function to draw the gun
def draw_gun():
    pygame.draw.rect(window, WHITE, gun)

# Function to move the gun
def move_gun():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and gun.x > 0:
        gun.move_ip(-5, 0)
    if keys[pygame.K_RIGHT] and gun.x < WIDTH - GUN_WIDTH:
        gun.move_ip(5, 0)
      

class BlueObject(pygame.Rect):
  def __init__(self, x, y):
      super().__init__(x, y, 20, 20)  # Blue object size
      self.color = (0, 0, 255)  # Blue color
      self.speed = 1  # Falling speed of the blue object
      self.has_shot = False  # Flag to track if the blue object has already shot
      self.shoot_cooldown = 60  # Cooldown between shots (adjust as needed)

  def shoot(self, player_rect):
      if not self.has_shot:
          player_center = (player_rect.x + player_rect.width // 2, player_rect.y + player_rect.height // 2)
          angle = calculate_angle((self.x, self.y), player_center)

          bullet_speed = 5  # Adjust as needed
          bullet_velocity = (bullet_speed * math.cos(angle), bullet_speed * math.sin(angle))

          new_bullet = BlueBullet(self.x + 10, self.y + 20, bullet_velocity)
          blue_bullets.append(new_bullet)

          self.has_shot = True  # Set the flag to indicate that the blue object has shot
          return True
      return False

  def move_blue_bullets(self):
    for bullet in blue_bullets:
        bullet.update_position()

  def update_cooldown(self):
      if not self.has_shot:
          self.shoot_cooldown -= 1
          if self.shoot_cooldown <= 0:
              self.has_shot = False  # Reset the flag for the next shot
              self.shoot_cooldown = 60  # Reset cooldown
# Class for blue object bullets
class BlueBullet(pygame.Rect):
  def __init__(self, x, y, velocity):
      super().__init__(x, y, bullet_width, bullet_height)
      self.color = (0, 0, 255)  # Blue color for the bullet
      self.velocity = velocity  # Bullet velocity

  def update_position(self):
      self.move_ip(self.velocity[0], self.velocity[1])

# Function to move blue object bullets
# Function to move blue object bullets
def move_blue_bullets():
  for bullet in blue_bullets:
      bullet.update_position()

# Function to check collisions between blue object bullets and the player
def check_blue_bullet_collisions():
  global running, game_over, show_game_over_message, current_score

  for bullet in blue_bullets:
      if player.colliderect(bullet):
          # Handle collision logic (e.g., decrease player health or set game over)
          running = False
          game_over = True
          show_game_over_message = True
          current_score = 0  # Reset the current score on game over
          game_over_state()  # Call the function to handle the game over state
          return

# class for power-ups
class PowerUp(pygame.Rect):
  def __init__(self, x, y):
      super().__init__(x, y, 10, 10)  # Power-up size
      self.color = (0, 255, 0)  # Green color
      self.duration = 10  # Duration in seconds
      self.collected = False  # Flag to track whether the power-up has been collected

power_ups = []



# Function to draw power-ups
def draw_power_ups():
    for power_up in power_ups:
        pygame.draw.rect(window, power_up.color, power_up)



# Function to move power-ups
def move_power_ups():
    for power_up in power_ups:
        if not power_up.collected:
            # Adjust the speed as needed
            power_up.move_ip(0, 2)

# Function to check collisions between player and power-ups
# Function to check collisions between player and power-ups
def check_power_up_collisions():
    global current_score, falling_speed, bullet_speed, score_multiplier, invincibility_duration, is_freeze_active

    for power_up in power_ups:
        if not power_up.collected and player.colliderect(power_up):
            power_up.collected = True
            current_score += 50  # Adjust the score as needed

            # Get a random power-up type
            power_up_type = random.choice(["speed", "freeze", "double_score", "invincibility"])
            apply_power_up_effects(power_up_type)

            power_ups.remove(power_up)  # Remove the power-up when collected
            return True

    return False
  
# Function to display power-up messages on the game window
# Function to display power-up messages on the game window
def show_power_up_message(message):
    message_font = pygame.font.Font(None, 36)
    message_text = message_font.render(message, True, (255, 255, 255))
    window.blit(message_text, (WIDTH // 2 - message_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    time.sleep(2)  # Display the message for 2 seconds (adjust as needed)
    window.fill((0, 0, 0))  # Clear the message from the window

def calculate_angle(start_point, end_point):
  angle = math.atan2(end_point[1] - start_point[1], end_point[0] - start_point[0])
  return angle

# Function to apply power-up effects
# Function to apply power-up effects
def apply_power_up_effects(power_up_type):
    global falling_speed, bullet_speed, score_multiplier, invincibility_duration, is_freeze_active

    if power_up_type == "freeze":
        time_freeze_duration = 5  # Example: Freeze falling objects for 5 seconds
        # Implement logic to freeze falling objects
        is_freeze_active = True
        show_power_up_message("Freeze Power-Up! Falling objects frozen for 5 seconds.")
        time.sleep(time_freeze_duration)
        is_freeze_active = False  # Deactivate freeze after the duration
    elif power_up_type == "double_score":
        double_score_active = True
        double_score_duration = 10  # Set the duration for the double score power-up (adjust as needed)
        show_power_up_message("Double Score Power-Up! Score multiplier doubled.")
    elif power_up_type == "invincibility":
        invincibility_active = True
        invincibility_duration = 10  # Set the duration for the invincibility power-up (adjust as needed)
        show_power_up_message("Invincibility Power-Up! Invincible for 10 seconds.")
# Function to draw bullets from the gun
def draw_bullets():
  for bullet in bullets:
      pygame.draw.rect(window, WHITE, bullet)  # Assuming WHITE color, adjust as needed

# Function to move bullets
def move_bullets():
    for bullet in bullets:
        bullet.move_ip(0, -bullet_speed)


# Function to check collisions between bullets and falling objects
def check_bullet_collisions():
  global current_score, game_over, show_game_over_message

  objects_to_remove = []  # Create a list to store objects that need to be removed

  for bullet in bullets:
      for obj in falling_objects:
          if bullet.colliderect(obj.rect):
              objects_to_remove.append((bullet, obj))  # Add the object pair to the removal list
              current_score += 100  # Increase the score for each destroyed object

  # Remove the objects after the iteration
  for bullet, obj in objects_to_remove:
      bullets.remove(bullet) if bullet in bullets else None
      falling_objects.remove(obj) if obj in falling_objects else None


# Move the shoot() method call inside the loop that updates blue objects
def move_blue_objects():
  global blue_objects
  for blue_object in blue_objects:
      blue_object.move_ip(0, int(falling_speed * 0.5))
      blue_object.update_cooldown()
      if blue_object.has_shot:
          blue_object.shoot(player)

def draw_blue_objects():
  for blue_object in blue_objects:
      pygame.draw.rect(window, blue_object.color, blue_object)

# Function to display level selection screen
def level_selection():
    window.fill((0, 0, 0))
    level_font = pygame.font.Font(None, 50)
    instructions_font = pygame.font.Font(None, 30)

    title_text = level_font.render("Select Difficulty Level", True, (255, 255, 255))
    window.blit(title_text, (WIDTH // 2 - 200, 50))

    instructions_text = instructions_font.render("Use Arrow Keys to Navigate, Enter to Confirm", True, (255, 255, 255))
    window.blit(instructions_text, (WIDTH // 2 - 230, 150))

    level_text = level_font.render(f"Level {current_level + 1}", True, (255, 255, 255))
    window.blit(level_text, (WIDTH // 2 - 50, HEIGHT // 2 - 25))

    pygame.display.flip()

# Display the level selection screen initially
level_selection()

# Level selection loop
selecting_level = True
while selecting_level:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_level = (current_level - 1) % len(difficulty_levels)
                level_selection()
            elif event.key == pygame.K_RIGHT:
                current_level = (current_level + 1) % len(difficulty_levels)
                level_selection()
            elif event.key == pygame.K_RETURN:
                selecting_level = False

    # Display the level selection screen
    level_selection()

# Set the chosen difficulty level
falling_speed = difficulty_levels[current_level]["falling_speed"]

# Function to draw the player
def draw_entities():
  pygame.draw.rect(window, WHITE, player)
  draw_gun()  # Draw the gun on top of the player

# Function to move the player and the gun
def move_player_and_gun():
    keys = pygame.key.get_pressed()
    if running and current_level != 7:
        if keys[pygame.K_LEFT] and player.x > 0:
            player.move_ip(-5, 0)
            gun.move_ip(-5, 0)  # Move the gun with the player
        if keys[pygame.K_RIGHT] and player.x < WIDTH - PLAYER_SIZE:
            player.move_ip(5, 0)
            gun.move_ip(5, 0)  # Move the gun with the player
    else:
        if running:
            if keys[pygame.K_LEFT] and player.x > 0:
                player.move_ip(-5, 0)
                gun.move_ip(-5, 0)  # Move the gun with the player
            if keys[pygame.K_RIGHT] and player.x < WIDTH - PLAYER_SIZE:
                player.move_ip(5, 0)
                gun.move_ip(5, 0)  # Move the gun with the player
            if keys[pygame.K_UP] and player.y > 0:
                player.move_ip(0, -5)
            if keys[pygame.K_DOWN] and player.y < HEIGHT - PLAYER_SIZE - GUN_HEIGHT:
                player.move_ip(0, 5)

# Function to reset the game state
def restart_game():
  global running, game_over, current_score, falling_objects, player, gun, bullets
  running = True
  game_over = False
  current_score = 0
  falling_objects = []
  bullets = []
  # Reset player and gun position
  player = pygame.Rect(WIDTH // 2 - PLAYER_SIZE // 2, HEIGHT - PLAYER_SIZE * 2, PLAYER_SIZE, PLAYER_SIZE)
  gun = pygame.Rect(WIDTH // 2 - GUN_WIDTH // 2, HEIGHT - GUN_HEIGHT - 30, GUN_WIDTH, GUN_HEIGHT)
    



# Function to draw falling objects
def draw_objects(objects):
    for obj in objects:
        pygame.draw.rect(window, RED, obj)

      # Function to move falling objects with adjustable speed based on player position
def move_objects(objects, player_y):
  for obj in objects:
      # Adjust falling speed based on the player's vertical position
      speed_factor = 1 + (player_y - HEIGHT / 2) / HEIGHT
      obj.move_ip(0, int(speed_factor * falling_speed))

# Function to update falling objects
def update_objects(objects):
  for obj in objects:
      # Check if the object has gone below the screen
      if obj.rect.y > HEIGHT:
          objects.remove(obj)  # Remove the object from the list if it's below the screen
  
# Function to check collisions between the player and falling objects

# Function to check collisions between the player and falling objects
def check_collisions():
  global running, game_over, show_game_over_message, current_score

  for obj in falling_objects:
      if player.colliderect(obj):
          return True, "Game Over!"

  for blue_object in blue_objects:
      if player.colliderect(blue_object):
          return True, "Game Over!"

  return False, ""

# Load font
font = pygame.font.Font(None, 36)

# Function to display pause screen
def pause_screen():
  window.fill((0, 0, 0))
  pause_font = pygame.font.Font(None, 50)
  instructions_font = pygame.font.Font(None, 30)

  pause_text = pause_font.render("Game Paused", True, (255, 255, 255))
  window.blit(pause_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))

  level_text = pause_font.render(f"Current Level: {current_level + 1}", True, (255, 255, 255))
  window.blit(level_text, (WIDTH // 2 - 150, HEIGHT // 2 + 0))

  instructions_text = instructions_font.render("         Q to Quit, R to Restart, N/M to Change Level", True, (255, 255, 255))
  window.blit(instructions_text, (WIDTH // 2 - 275, HEIGHT // 2 + 50))

  pygame.display.flip()
  
# Function to handle the game over state
def game_over_state():
  global show_game_over_message, running, game_over, current_score, falling_objects, player

  # Display "Game Over!" message outside the main game loop
  while show_game_over_message:
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              pygame.quit()
              sys.exit()
          elif event.type == pygame.KEYDOWN:
              if event.key == pygame.K_r:
                  restart_game()
                  show_game_over_message = False

      window.fill((0, 0, 0))
      game_over_text = font.render("Game Over!", True, (255, 255, 255))
      window.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 18))
      # Display "Press R to Restart" message
      restart_text = font.render("Press R to Restart", True, (255, 255, 255))
      window.blit(restart_text, (WIDTH // 2 - 120, HEIGHT // 2 + 50))
      pygame.display.flip()

  # Reset the game state
  running = True
  game_over = False
  current_score = 0
  falling_objects = []
  player = pygame.Rect(WIDTH // 2 - PLAYER_SIZE // 2, HEIGHT - PLAYER_SIZE * 2, PLAYER_SIZE, PLAYER_SIZE)








# Main game loop
while True:
  current_time = pygame.time.get_ticks()
  red_obstacles = []
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
      elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_p:
              paused = not paused
              if paused:
                  pause_screen()
          elif event.key == pygame.K_q:
              pygame.quit()
              sys.exit()
          elif event.key == pygame.K_r:
              restart_game()
          elif event.key == pygame.K_1:
            bot_active = not bot_active
          

  
          
          elif event.key == pygame.K_n and paused:  # Change level to the left in pause screen
              current_level = (current_level - 1) % len(difficulty_levels)
              falling_speed = difficulty_levels[current_level]["falling_speed"]
              pause_screen()
          elif event.key == pygame.K_m and paused:  # Change level to the right in pause screen
              current_level = (current_level + 1) % len(difficulty_levels)
              falling_speed = difficulty_levels[current_level]["falling_speed"]
              pause_screen()
            
  

  move_player_and_gun()

  # Bot logic
  if bot_active:
      # Find the closest falling object
      closest_object = None
      min_distance = float('inf')

      for obj in falling_objects:
          distance = abs(gun.x - obj.x)
          if distance < min_distance:
              min_distance = distance
              closest_object = obj

      # Move towards the closest object if it's within the screen boundaries
      if closest_object and 0 <= closest_object.x <= WIDTH - closest_object.width:
          target_x = closest_object.x

          # Move the player's main rectangle
          if player.x < target_x:
              player.move_ip(5, 0)
          elif player.x > target_x:
              player.move_ip(-5, 0)

          # Move the gun
          if gun.x < target_x:
              gun.move_ip(5, 0)
          elif gun.x > target_x:
              gun.move_ip(-5, 0)

          # Shoot bullets constantly
          if current_time - last_shot_time > SHOOT_COOLDOWN:
              new_bullet = pygame.Rect(player.x + PLAYER_SIZE // 2 - bullet_width // 2, player.y - bullet_height, bullet_width, bullet_height)
              bullets.append(new_bullet)
              last_shot_time = current_time  # Update the last shot time

  if not paused:

    # Check for continuous shooting with cooldown
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not paused and (current_time - last_shot_time) > SHOOT_COOLDOWN:
        new_bullet = pygame.Rect(player.x + PLAYER_SIZE // 2 - bullet_width // 2, player.y - bullet_height, bullet_width, bullet_height)
        bullets.append(new_bullet)
        last_shot_time = current_time  # Update the last shot time

  

  if not paused:
      keys = pygame.key.get_pressed()
      if running and current_level != 7:
        if keys[pygame.K_LEFT] and player.x > 0:
          player.move_ip(-5, 0)
          gun.move_ip(-5, 0)
        if keys[pygame.K_RIGHT] and player.x < WIDTH - PLAYER_SIZE:
          player.move_ip(5, 0)
          gun.move_ip(5, 0)
      else:
        if running:
          if keys[pygame.K_LEFT] and player.x > 0:
            player.move_ip(-5, 0)
            gun.move_ip(-5, 0)
          if keys[pygame.K_RIGHT] and player.x < WIDTH - PLAYER_SIZE:
            player.move_ip(5, 0)
            gun.move_ip(5, 0)
          if keys[pygame.K_UP] and player.y > 0:  # Allow the player to move up
            player.move_ip(0, -5)
            gun.move_ip(0, -5)
          if keys[pygame.K_DOWN] and player.y < HEIGHT - PLAYER_SIZE:  # Allow the player to move down
            player.move_ip(0, 5)
            gun.move_ip(0, 5)

        # Generate a new falling object or power-up randomly
      

      if current_level >= 3 and current_level <= 5:
        if random.randint(1, 120) == 1 and running:
          new_blue_object = BlueObject(random.randint(0, WIDTH - 20), 0)
          blue_objects.append(new_blue_object)

        if current_level != 5:
          if random.randint(1, 30) == 1 and running:
            if random.randint(1, 60) == 1:  # 1 in 50 chance for a power-up
                new_power_up = PowerUp(random.randint(0, WIDTH - 10), 0)
                power_ups.append(new_power_up)
            else:
                new_object = FallingObject(random.randint(0, WIDTH - 20), 0, 20, 20, RED)
                falling_objects.append(new_object)

        if current_level == 5:
          if random.randint(1, 16) == 1 and running:
              if random.randint(1, 60) == 1:  # 1 in 50 chance for a power-up
                  new_power_up = PowerUp(random.randint(0, WIDTH - 10), 0)
                  power_ups.append(new_power_up)
              else:
                  new_object = FallingObject(random.randint(0, WIDTH - 20), 0, 20, 20, RED)
                  falling_objects.append(new_object)
          
      else:
        if random.randint(1, 30) == 1 and running:
          if random.randint(1, 3) == 1:  # 1 in 50 chance for a power-up
              new_power_up = PowerUp(random.randint(0, WIDTH - 10), 0)
              power_ups.append(new_power_up)
          else:
            new_object = FallingObject(random.randint(0, WIDTH - 20), 0, 20, 20, RED)
            falling_objects.append(new_object)




      if running:
          current_score += 1  # Increment the score as the game progresses
            # Update high score if the current score is higher
          high_score = max(high_score, current_score)

        # Display current and high scores
      score_text = font.render(f"Score: {current_score}  High Score: {high_score}", True, (255, 255, 255))
      window.blit(score_text, (10, 10))

        # Move and draw falling objects with the specified speed for the current difficulty level
      if running and current_level != 7:
          move_objects(falling_objects, falling_speed)
      else:
        if running:
          move_objects(falling_objects, player.y)

        # Check collisions
      collision, message = check_collisions()
      if collision and not game_over:
          running = False
          game_over = True
            # Reset the current score on game over
          current_score = 0  # Set game_over to True when the game ends

      # Update blue objects position, shoot, and check collisions
      for blue_object in blue_objects:
        blue_object.move_ip(0, int(falling_speed * 0.5))
        blue_object.update_cooldown()
        blue_object.shoot(player)

      # Check collisions between blue object bullets and player
      for bullet in bullets:
          for blue_object in blue_objects:
              if bullet.colliderect(blue_object):
                  # Handle collision logic (e.g., decrease player health)
                  bullets.remove(bullet)

      if running:
        window.fill((0, 0, 0))

        # Draw player and falling objects
      draw_entities()
      draw_gun()
      draw_objects(falling_objects)

      if running:
        move_blue_objects()
        draw_blue_objects()
        # Update blue object bullets position and check collisions
        move_blue_bullets()
        check_blue_bullet_collisions()

      for bullet in blue_bullets:
        pygame.draw.rect(window, bullet.color, bullet)
      

      if not paused:
        move_bullets()
        check_bullet_collisions()
        draw_bullets()
        # Check collisions between bullets and falling objects
      

      if check_power_up_collisions():
        pass


        # Draw the black rectangle on top
      if current_level == 6:
          pygame.draw.rect(window, (0, 0, 0), pygame.Rect(0, 0, WIDTH, HEIGHT // 2))

        # Display current and high scores
      if running:
        score_text = font.render(f"Score: {current_score}  High Score: {high_score}", True, (255, 255, 255))
        window.blit(score_text, (10, 10))

        # Draw the level information last
      if not game_over:
        level_text = font.render(f"Current Level: {current_level + 1}", True, (255, 255, 255))
        window.blit(level_text, (WIDTH // 2 - 150, HEIGHT // 2 + 0))

          # Update the display
        pygame.display.flip()


        # Control the frame rate
      clock.tick(FPS)
        # Check for game over condition
      if game_over and not show_game_over_message:
          show_game_over_message = True
          game_over_state()  # Call the function to handle the game over stateover_message = True
