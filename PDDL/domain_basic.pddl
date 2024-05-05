(define (domain seidor)
    (:requirements :strips :fluents :typing :equality :disjunctive-preconditions :universal-preconditions :quantified-preconditions :negative-preconditions )

(:types 
    shelving cell product person - object
    aisle cash - cell
)

(:predicates  
    (acces_to ?a -aisle ?t -shelving)
    (adjacent ?c1 -cell ?c2 -cell)
    (inside ?p -product ?s -shelving)
    (holding ?pr -product) 
    (in ?p -person ?c -cell)
)

(:functions
    (total_meters)
)

(:action Move
    :parameters (?p -person ?c_ini -cell ?c_fi -cell)
    :precondition (and (in ?p ?c_ini) (or (adjacent ?c_ini ?c_fi) (adjacent ?c_fi ?c_ini)) (in ?p ?c_ini)) 
    :effect (and (not(in ?p ?c_ini))(in ?p ?c_fi)(increase (total_meters) 1)) ;El combustible de rover disminueix en 1 i el combustible gastat total augmenta
)


(:action Pick_Product
    :parameters (?p -person ?a -aisle ?s -shelving ?pr -product)
    :precondition (and (in ?p ?a)
                        (acces_to ?a ?s)
                        (inside ?pr ?s)
                        (not(holding ?pr)))
                        
    :effect (and (holding ?pr))
    )
)




