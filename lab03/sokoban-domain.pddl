; Problem definition of the Sokoban domain.

(define (domain sokoban-teleport)

(:requirements :strips :negative-preconditions)

(:predicates
    ; Player x.
    (PLAYER ?x)

    ; Crate x.
    (CRATE ?x)

    ; Position x is adjacent to position y.
    (is-adjacent ?x ?y)

    ; Position x, y, z are on the same line.
    (is-aligned ?x ?y ?z)

    ; Position x is free.
    (is-free ?x)

    ; Player teleported.
    (has-teleported)

    ; Has crate in location x.
    (has-crate ?x)

    ; Object x located at position y.
    (at ?x ?y)
)

(:action move
    :parameters (?player ?current_position ?next_position)
    :precondition (and
        ; Is ?player a player?
        (PLAYER ?player)

        ; Is the next position free?
        (is-free ?next_position)

        ; Is the ?player at current position?
        (at ?player ?current_position)

        ; Is the move from current to next position valid?
        (is-adjacent ?current_position ?next_position)
    )
    :effect (and
        ; Move player to next position.
        (at ?player ?next_position)
        (not (at ?player ?current_position))

        ; Mark previous position as free.
        (is-free ?current_position)
        (not (is-free ?next_position))
    )
)

(:action push
    :parameters (?player ?crate ?player_position ?crate_position ?next_position)
    :precondition (and
        ; Is ?player a player?
        (PLAYER ?player)

        ; Is ?player at ?player_position?
        (at ?player ?player_position)

        ; Is ?crate a crate?
        (CRATE ?crate)

        ; Is ?crate at ?crate_position?
        (at ?crate ?crate_position)
        (has-crate ?crate_position)

        ; Is ?next_position free?
        (is-free ?next_position)

        ; Is ?player_position, ?crate_position and ?next_position on the same line and next to each other?
        (is-adjacent ?player_position ?crate_position)
        (is-adjacent ?crate_position ?next_position)
        (is-aligned ?player_position ?crate_position ?next_position)
    )
    :effect (and
        ; Move player to crate and mark the location as free.
        (at ?player ?crate_position)
        (not (at ?player ?player_position))
        (is-free ?player_position)

        ; Move crate to next position.
        (at ?crate ?next_position)
        (has-crate ?next_position)
        (not (at ?crate ?crate_position))
        (not (has-crate ?crate_position))
        (not (is-free ?next_position))
    )
)

(:action teleport
    :parameters (?player ?current_position ?next_position)
    :precondition (and
        ; Is ?player a player?
        (PLAYER ?player)

        ; Is the next position free?
        (is-free ?next_position)

        ; Is the ?player at current position?
        (at ?player ?current_position)

        ; ?player must not have teleported earlier.
        (not (has-teleported))
    )
    :effect (and
        ; Move player to next position.
        (at ?player ?next_position)
        (not (at ?player ?current_position))

        ; Mark previous position as free.
        (is-free ?current_position)
        (not (is-free ?next_position))

        ; Set has-teleported to true.
        (has-teleported)
    )
)

)