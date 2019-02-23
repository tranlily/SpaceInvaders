import sys
from time import sleep

import pygame
import random

from bullet import Bullet
from alien import Alien
from score import Score
from ufo import Ufo


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, ufos, bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, ufos, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, ufos, bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        ufos.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet, if limit not reached yet."""
    # Create a new bullet, add to bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)

        # SOUND FX GOES HEREEEEEEE
        bullets.add(new_bullet)

def initialize_screen(screen):
    # render images
    enemyA = pygame.image.load('images/alienA.png')
    screen.blit(enemyA, [375, 275])

    enemyC = pygame.image.load('images/alienC.png')
    screen.blit(enemyC, [375, 325])

    enemyB = pygame.image.load('images/alienB.png')
    screen.blit(enemyB, [375, 375])

    enemyD = pygame.image.load('images/ufo.png')
    screen.blit(enemyD, [375, 425])

    myfont = pygame.font.SysFont("monospace", 125)
    myfont_newline = pygame.font.SysFont("monospace", 75)
    point_font = pygame.font.SysFont("monospace", 40)

    # render text
    label = myfont.render("SPACE", 200, (229, 238, 250))
    screen.blit(label, (350, 100))

    label_newline = myfont_newline.render("INVADERS", 200, (76, 215, 255))
    screen.blit(label_newline, (355, 175))

    pointA = point_font.render(" = 10 PTS ", 200, (229, 238, 250))
    screen.blit(pointA, (440, 280))

    pointB = point_font.render(" = 25 PTS ", 200, (229, 238, 250))
    screen.blit(pointB, (440, 330))

    pointC = point_font.render(" = 50 PTS ", 200, (229, 238, 250))
    screen.blit(pointC, (440, 380))

    pointD = point_font.render(" = ??? ", 200, (229, 238, 250))
    screen.blit(pointD, (440, 430))


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, ufos, play_button, score_button):
    """Update images on the screen, and flip to the new screen."""
    # Redraw the screen, each pass through the loop.
    screen.fill(ai_settings.bg_color)

    # Redraw all bullets, behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Draw ufos

    ufo_event_check(ai_settings, screen, ufos)
    ufos.draw(screen)

    # Draw the score information.
    sb.show_score()

    # Draw the play button and home screen if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()
        score_button.draw_button()
        initialize_screen(screen)


    # Make the most recently drawn screen visible.
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, ufos, bullets):
    """Update position of bullets, and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, ufos, bullets)


def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

# This checks for aliens and ufos
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, ufos, bullets):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level.
        bullets.empty()
        ai_settings.increase_speed()

        # Increase level.
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)

    ufo_collisions = pygame.sprite.groupcollide(bullets, ufos, True, True)
    if ufo_collisions:
        for ufos in ufo_collisions.values():
            stats.score += ai_settings.ufo_points * len(ufos)
            sb.prep_score()
        check_high_score(stats, sb)


def check_fleet_edges(ai_settings, aliens, ufos):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

    for ufo in ufos.sprites():
        if ufo.check_edges():
            ai_settings.ufo_direction *= -1


def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet, and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1

        # Update scoreboard.
        sb.prep_ships()

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

    # Empty the list of aliens and bullets.
    aliens.empty()
    bullets.empty()


    # Create a new fleet, and center the ship.
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

    # Pause.
    sleep(0.5)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


# Update aliens and ufos.
def update_aliens(ai_settings, screen, stats, sb, ship, aliens, ufos, bullets):
    check_fleet_edges(ai_settings, aliens, ufos)

    aliens.update()
    ufos.update()

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height - (5 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien_C(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien, and place it in the row."""
    img = 'images/alienC.png'
    img2 = 'images/alienC2.png'
    alienC = Alien(ai_settings, screen, img, img2)
    alien_width = alienC.rect.width
    alienC.x = alien_width + 2 * alien_width * alien_number
    alienC.rect.x = alien_width + 2 * alien_width * alien_number
    alienC.rect.y = alienC.rect.height + 2 * alienC.rect.height * row_number
    aliens.add(alienC)



def create_alien_B(ai_settings, screen, aliens, alien_number, row_number):
    img = 'images/alienB.png'
    img2 = 'images/alienB2.png'
    alienB = Alien(ai_settings, screen, img, img2)
    alien_width = alienB.rect.width
    alienB.x = alien_width + 2 * alien_width * alien_number
    alienB.rect.x = alien_width + 2 * alien_width * alien_number
    alienB.rect.y = alienB.rect.height + 2 * alienB.rect.height * row_number
    aliens.add(alienB)



def create_alien_A(ai_settings, screen, aliens, alien_number, row_number):
    img = 'images/alienA.png'
    img2 = 'images/alienA2.png'

    # When putting in the img variable, it will be white instead of orange.
    alienA = Alien(ai_settings, screen, img, img2)
    alien_width = alienA.rect.width
    alienA.x = alien_width + 2 * alien_width * alien_number
    alienA.rect.x = alien_width + 2 * alien_width * alien_number
    alienA.rect.y = alienA.rect.height + 2 * alienA.rect.height * row_number
    aliens.add(alienA)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien, and find number of aliens in a row.
    img = 'images/alienC.png'
    img2 = 'images/alienC.png'

    alien = Alien(ai_settings, screen, img, img2)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Create the fleet of aliens.
    for row_number in range(1, number_rows - 3):
        for alien_number in range(number_aliens_x):
            create_alien_B(ai_settings, screen, aliens, alien_number, row_number)

    # Create the fleet of aliens.
    for row_number in range(number_rows - 3, number_rows - 1):
        for alien_number in range(number_aliens_x):
            create_alien_C(ai_settings, screen, aliens, alien_number, row_number)

    # Create the fleet of aliens.
    for row_number in range(number_rows - 1, number_rows+1):
        for alien_number in range(number_aliens_x):
            create_alien_A(ai_settings, screen, aliens, alien_number, row_number)

def create_ufo(ai_settings, screen):
    ufo = None
    if random.randrange(0, 100) <= 50:
        ufo = Ufo(ai_settings, screen)

    time_stamp = pygame.time.get_ticks()
    return time_stamp, ufo

def ufo_event_check(ai_settings, screen, ufos):
    if not ai_settings.last_ufo and not ufos:
        ai_settings.last_ufo, ufo = create_ufo(ai_settings, screen)
        if ufo:
            ufos.add(ufo)
    elif abs(pygame.time.get_ticks() - ai_settings.last_ufo) > ai_settings.ufo_min_interval and not ufos:
        ai_settings.last_ufo, ufo = create_ufo(ai_settings, screen)
        if ufo:
            ufos.add(ufo)
