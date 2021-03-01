(define (problem monkey_problem)

(:domain one_monkey_one_banana_domain)
(:objects m b c)

(:init
    (is_banana b)
    (is_chair c)
)

(:goal (and
    (monkey_ate_banana)
)
)

)
