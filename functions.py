import time
from random import randint
import sys
import pygame as pg
from bullet import Bullet
from alien import Alien
from star import Star
from boss import Boss


def check_events(fmt_settings, screen, stats, sb, play_button, ship, aliens, bullets, perks):
    """Respond to keypresses and mouse movements"""

    for event in pg.event.get():
        # print("bullet wdith", fmt_settings.bullet_width)
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.KEYDOWN:
            check_keydown_events(event, fmt_settings, screen, stats, sb, ship, aliens, bullets, perks)
        elif event.type == pg.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()
            check_play_button(fmt_settings, screen, stats, sb, ship, aliens, bullets, perks)


def check_play_button(fmt_settings, screen, stats, sb, ship, aliens, bullets, perks):
    """Start a new game when player clicks Play"""

    # Reset game settings
    fmt_settings.initialize_dynamic_settings()

    # Reset game
    stats.reset_stats()
    stats.game_active = True

    # Reset scoreboard
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()

    aliens.empty()
    bullets.empty()
    perks.empty()

    create_fleet(fmt_settings, screen, ship, aliens, perks)
    ship.center_ship()

    """
        if play_button.rect.collidepoint(mouse_x, mouse_y):
        button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and not stats.game_active:
            # Reset game settings
            fmt_settings.initialize_dynamic_settings()

            # Hide mouse cursor
            pg.mouse.set_visible(False)

            # Reset game
            stats.reset_stats()
            stats.game_active = True

            # Reset scoreboard
            sb.prep_score()
            sb.prep_high_score()
            sb.prep_level()
            sb.prep_ships()

            aliens.empty()
            bullets.empty()
            perks.empty()

            create_fleet(fmt_settings, screen, ship, aliens, perks)
            ship.center_ship()

    """


def check_keydown_events(event, fmt_settings, screen, stats, sb, ship, aliens, bullets, perks):
    """Respond to key presses"""
    # print("bullet wdith", fmt_settings.bullet_width)
    if event.key == pg.K_RIGHT:
        # Move ship to right
        ship.moving_right = True
    elif event.key == pg.K_LEFT:
        # Move ship left
        ship.moving_left = True
    elif event.key == pg.K_SPACE:
        fire_bullet(fmt_settings, screen, ship, stats, bullets)
    elif event.key == pg.K_ESCAPE:
        # save high score
        with open('_highscore.txt', 'w') as reader:
            # write current high score to file
            reader.write((str(stats.high_score)))
        sys.exit()
    elif event.key == pg.K_p:
        if not stats.game_active:
            check_play_button(fmt_settings, screen, stats, sb, ship, aliens, bullets, perks)


def check_keyup_events(event, ship):
    """Respond to key releases"""

    if event.key == pg.K_RIGHT:
        ship.moving_right = False
    elif event.key == pg.K_LEFT:
        ship.moving_left = False


def check_bullet_alien_collisions(fmt_settings, screen, stats, sb, ship, aliens, bullets, perks):
    """Respond to bullet-alien collisions"""

    perk_off = True
    if 'super_bullet' in stats.perks_active:
        perk_off = False

    # Check for bullets that hit aliens; remove bullets and aliens that meet this criteria
    collisions = pg.sprite.groupcollide(bullets, aliens, perk_off, True)  # perk is for the super bullet perk,
    # if super bullet active then perk is true

    if collisions:
        for aliens in collisions.values():
            # Check for perks
            for alien in aliens:
                if alien.classification != 'default':
                    stats.perks_active.append(alien.classification)

            # Modify Score
            stats.score += fmt_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # Remove existing bullets, speed up game, and make new fleet (start new level)
        bullets.empty()
        fmt_settings.increase_speed(stats)

        # Increase level
        stats.level += 1
        sb.prep_level()

        create_fleet(fmt_settings, screen, ship, aliens, perks)


def check_high_score(stats, sb):
    """Check to see if there's a new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_fleet_edges(fmt_settings, aliens):
    """Respond appropriately if any aliens have reached an edge"""

    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(fmt_settings, aliens)
            break


def check_aliens_bottom(fmt_settings, screen, stats, sb, ship, aliens, bullets, perks):
    """Check if any aliens have reached the bottom of the screen"""

    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(fmt_settings, screen, stats, sb, ship, aliens, bullets, perks)
            stats.game_active = False
            break


def update_bullets(fmt_settings, screen, stats, sb, ship, aliens, bullets, perks):
    """Update position of bullets and remove old ones"""

    # Update bullet position
    bullets.update()

    # Remove bullets that go off-screen
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(fmt_settings, screen, stats, sb, ship, aliens, bullets, perks)


def update_aliens(fmt_settings, screen, stats, sb, ship, aliens, bullets, perks):
    """Check if the fleet is at and edge, then update positions of aliens in fleet"""

    check_fleet_edges(fmt_settings, aliens)
    aliens.update()

    # Search for alien-ship collisions
    if pg.sprite.spritecollideany(ship, aliens):
        ship_hit(fmt_settings, screen, stats, sb, ship, aliens, bullets, perks)

    # Look for aliens at screen bottom
    check_aliens_bottom(fmt_settings, screen, stats, sb, ship, aliens, bullets, perks)


def update_screen(fmt_settings, screen, stats, sb, ship, aliens, stars, bullets, play_button):
    """Update images on screen and flip to new screen"""

    #  Redraw screen everytime you go through the while loop
    screen.fill(fmt_settings.bg_color)
    # Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    stars.draw(screen)
    sb.show_score()

    # Draw play button if game is inactive
    if not stats.game_active:
        play_button.draw_button()

    #  Make most recent screen available
    pg.display.flip()


def fire_bullet(fmt_settings, screen, ship, stats, bullets):
    """Fire a bullet if under limit"""

    # Check for perk
    perk_active = 'super_bullet' in stats.perks_active
    perk = False
    loc = 0

    if perk_active:
        perk = True
        loc = stats.perks_active.index('super_bullet')
        
    # Create new bullet and add it to bullet group
    if len(bullets) < fmt_settings.bullets_allowed:
        new_bullet = Bullet(fmt_settings, screen, ship, perk)
        bullets.add(new_bullet)

        # Get rid of the used perk
        if perk_active & len(stats.perks_active) >= 1:
            del stats.perks_active[loc]



def play_sound(sound, duration):
    """Play a certain sound for a specific duration
    sound: a Sound object that is to be played
    duration: amount of time in seconds to wait before shutting off the sound

    """

    sound.play()
    time.sleep(duration)
    sound.stop()


def create_fleet(fmt_settings, screen, ship, aliens, perks):
    """Create a fleet of aliens"""

    # Create alien and find number of aliens in a row
    # Space between each alien is equal to one alien width

    alien = Alien(fmt_settings, screen)
    num_aliens_x = get_num_objs_x(fmt_settings, alien.rect.width)
    num_rows = get_num_rows(fmt_settings, ship.rect.height, alien.rect.height)

    # Create alien fleet
    for row_number in range(num_rows):
        for alien_number in range(num_aliens_x):
            create_alien(fmt_settings, screen, aliens, alien_number, row_number, perks)


def create_stars(fmt_settings, screen, ship, stars, padding):
    """Create background of stars"""

    star = Star(fmt_settings, screen)
    num_stars_x = get_num_objs_x(fmt_settings, star.rect.width, padding)
    num_rows = get_num_rows(fmt_settings, ship.rect.height, star.rect.height, padding)

    # Create stars
    for row_number in range(num_rows):
        for star_number in range(num_stars_x):
            x = randint(-80, 80)
            y = randint(-50, 50)

            create_star(fmt_settings, screen, stars, star_number, row_number, padding, x, y)


def create_alien(fmt_settings, screen, aliens, alien_number, row_number, perks):
    """Create an alien and put it in the row"""

    seed = randint(1, 10)
    classification = 'default'
    if len(perks) < fmt_settings.perks_allowed:
        if seed == 1:
            classification = 'shield'
            fmt_settings.perks_allowed += 1
        elif seed == 3:
            classification = 'super_bullet'
            fmt_settings.perks_allowed += 1
        elif seed == 7:
            classification = 'extra_life'
            fmt_settings.perks_allowed += 1

    alien = Alien(fmt_settings, screen, classification)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
    perks.add(alien)


def create_star(fmt_settings, screen, stars, star_number, row_number, padding, x=0, y=0):
    """Create a star and put it in the row"""

    star = Star(fmt_settings, screen)
    star_width = star.rect.width
    star.x = star_width + padding * star_width * star_number + x
    star.rect.x = star.x
    star.rect.y = star.rect.height + padding * star.rect.height * row_number + y
    stars.add(star)


def get_num_objs_x(fmt_settings, obj_width, padding=2):
    """Determine the number of objects that fit in a row

    """

    available_space_x = fmt_settings.screen_width - padding * obj_width
    num_aliens_x = int(available_space_x / (padding * obj_width))

    return num_aliens_x


def get_num_rows(fmt_settings, ship_height, obj_height, padding=3):
    """Find the number of rows of objects that can fit on the screen"""

    available_space_y = (fmt_settings.screen_height - (3 * obj_height) - ship_height)
    num_rows = int(available_space_y / (2 * obj_height))

    return num_rows


def change_fleet_direction(fmt_settings, aliens):
    """Drop the entire fleet and change its direction"""

    for alien in aliens.sprites():
        alien.rect.y += fmt_settings.fleet_drop_speed
    fmt_settings.fleet_direction *= -1


def ship_hit(fmt_settings, screen, stats, sb, ship, aliens, bullets, perks):
    """Respond to ship being hit by an alien"""

    play_sound(ship.death_sound, 0.5)
    if stats.ships_left > 0:
        # Decrease ships_left
        stats.ships_left -= 1

        # Update scoreboard
        sb.prep_ships()

        # Empty list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create new fleet and center ship
        create_fleet(fmt_settings, screen, ship, aliens, perks)
        ship.center_ship()

        # Pause
        time.sleep(0.5)
    else:
        stats.game_active = False
        pg.mouse.set_visible(True)



