; Single monkey finding and eating a single banana in a room.

(define (domain one_monkey_one_banana_domain)

(:requirements :strips :negative-preconditions)

(:predicates
    (is_banana ?x)
    (is_chair ?x)
    (at ?x)
    (has_chair)
    (monkey_ate_banana)
)

; Action to go to the chair.
(:action go-to-chair
    :parameters (?x)
    :precondition (and
        (is_chair ?x)
    )
    :effect (and
        (at ?x)
    )
)

; Action to carry chair.
(:action pickup-chair
    :parameters (?x)
    :precondition (and
        (is_chair ?x)
        (at ?x)
    )
    :effect (and
        (has_chair)
    )
)

; Action to go to banana.
(:action go-to-banana
    :parameters (?x)
    :precondition (and
        (is_banana ?x)
        (has_chair)
    )
    :effect (and
        (at ?x)
    )
)

; Action to eat banana.
(:action have-banana
    :parameters (?x)
    :precondition (and
        (is_banana ?x)
        (at ?x)
        (has_chair)
    )
    :effect (and
        (monkey_ate_banana)
    )
)
)