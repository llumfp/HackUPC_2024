(define (problem store_problem) ; Nombre del problema.
    (:domain practica2_2) ; Nombre del dominio al que se asocia este problema.

    (:objects
        shelf1 shelf2 - shelving
        cell1 cell2 cell3 - aisle
        cashier -cash
        prod1 prod2 - product
        person1 - person
    )

    (:init
        (acces_to cell2 shelf1)
        (adjacent cell1 cell2)
        (adjacent cell2 cell3)
        (adjacent cell3 cashier)
        (inside prod1 shelf1)
        (inside prod2 shelf1)
        (in person1 cashier)
        (= (total_meters) 0)
    )

    (:goal
        (and
            (in person1 cashier)
            (holding prod2)
        )
    )
)

;.\metricff -o domain_basic.pddl -f problem_basic.pddl -O > output.txt