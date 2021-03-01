; Problem definition of the Sokoban domain.

(define (domain sokoban-teleport)

(:requirements :strips :negative-preconditions)

(:predicates
    ; Player x.
    (is-player ?x)

    ; Crate x.
    (is-crate ?x)

    ; Position x is adjacent to position y.
    (is-adjacent ?x ?y)

    ; Position x, y, z are on the same line.
    (is-aligned ?x ?y ?z)

    ; Position x is free.
    (is-free ?x)

    ; Player teleported.
    (has-teleported)

    ; Object y located at position x.
    (object-at ?x ?y)
)

(:action move
    :parameters (?player ?current_position ?next_position)
    :precondition (and
        ; Is ?player a player?
        (is-player ?player)

        ; Is the next position free?
        (is-free ?next_position)

        ; Is the ?player at current position?
        (object-at ?player ?current_position)

        ; Is the move from current to next position valid?
        (is-adjacent ?current_position ?next_position)
    )
    :effect (and
        ; Move player to next position.
        (object-at ?player ?next_position)
        (not (object-at ?player ?current_position))

        ; Mark previous position as free.
        (is-free ?current_position)
        (not (is-free ?next_position))
    )
)

(:action push
    :parameters (?player ?crate ?player_position ?crate_position ?next_position)
    :precondition (and
        ; Is ?player a player?
        (is-player ?player)

        ; Is ?player at ?player_position?
        (object-at ?player ?player_position)

        ; Is ?crate a crate?
        (is-crate ?crate)

        ; Is ?crate at ?crate_position?
        (object-at ?crate ?crate_position)

        ; Is ?next_position free?
        (is-free ?next_position)

        ; Is ?player_position, ?crate_position and ?next_position on the same line and next to each other?
        (is-adjacent ?player_position ?crate_position)
        (is-adjacent ?crate_position ?next_position)
        (is-aligned ?player_position ?crate_position ?next_position)
    )
    :effect (and
        ; Move player to crate and mark the location as free.
        (object-at ?player ?crate_position)
        (not (object-at ?player ?player_position))
        (is-free ?player_position)

        ; Move crate to next position.
        (object-at ?crate ?next_position)
        (not (object-at ?crate ?crate_position))
        (not (is-free ?next_position))
    )
)

(:action teleport
    :parameters (?player ?current_position ?next_position)
    :precondition (and
        ; Is ?player a player?
        (is-player ?player)

        ; Is the next position free?
        (is-free ?next_position)

        ; Is the ?player at current position?
        (object-at ?player ?current_position)

        ; ?player must not have teleported earlier.
        (not (has-teleported))
    )
    :effect (and
        ; Move player to next position.
        (object-at ?player ?next_position)
        (not (object-at ?player ?current_position))

        ; Mark previous position as free.
        (is-free ?current_position)
        (not (is-free ?next_position))

        ; Set has-teleported to true.
        (has-teleported)
    )
)

)