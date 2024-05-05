(define (problem store_problem) ; Nombre del problema.
    (:domain practica2_2) ; Nombre del dominio al que se asocia este problema.

    (:objects
        shelf1 shelf2 shelf3 shelf4 shelf5 shelf6 shelf7 shelf8 shelf9 shelf10 shelf11 shelf12 shelf13 shelf14 shelf15 shelf16 shelf17 shelf18 shelf19 shelf20 - shelving
        cell1 cell2 cell3 cell4 cell5 cell6 cell7 cell8 cell9 cell10 cell11 cell12 cell13 cell14 cell15 cell16 cell17 cell18 cell19 cell20 cell21 cell22 cell23 cell24 cell25 cell26 cell27 cell28 cell29 cell30 cell31 cell32 cell33 cell34 cell35 cell36 cell37 cell38 cell39 cell40 cell41 cell42 cell43 cell44 cell45 cell46 cell47 cell48 cell49 cell50 cell51 cell52 cell53 cell54 cell55 cell56 cell57 cell58 cell59 cell60 cell61 cell62 cell63 cell64 cell65 cell66 cell67 cell68 cell69 cell70 cell71 cell72 cell73 cell74 cell75 cell76 cell77 cell78 cell79 cell80 - aisle
        cashier -cash
        prod1 prod2 - product; modificar 
        person1 - person
    )

    (:init
        (acces_to cell2 shelf1) ;falta
        (adjacent cell1 cell2) ;falta
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