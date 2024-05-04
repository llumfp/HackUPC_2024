(define (problem practica2_2)
(:domain practica2_2)
(:objects 
    R1 R2 -rover
    As1 As2 As3 As4 -asentamiento
    Al1 Al2 Al3 -almacen
)

(:init
    (Adyacente As1 As2)
    (Adyacente As3 As4)
    (Adyacente As2 As3)
    (Adyacente As4 Al1)
    (Adyacente Al1 Al2)
    (Adyacente Al2 Al3)
    (Adyacente Al3 As1)
    (En R1 Al1) (= (Suministros_rover R1) 0) (= (Personal_rover R1) 0)
    (En R2 As1) (= (Suministros_rover R2) 0) (= (Personal_rover R2) 0)
    (= (Combustible R1) 20)
    (= (Combustible R2) 20)
    (= (Total_combustible_gastat) 0)
    (= (Requerimiento_personal As1) 0)
    (= (Requerimiento_personal As2) 0)
    (= (Requerimiento_personal As3) 3)
    (= (Requerimiento_personal As4) 4)
    (= (Requerimiento_suministro As1) 0)
    (= (Requerimiento_suministro As2) 0)
    (= (Requerimiento_suministro As3) 2)
    (= (Requerimiento_suministro As4) 0)
    (= (Personal_asentamiento As1) 1)
    (= (Personal_asentamiento As2) 0)
    (= (Personal_asentamiento As3) 0)
    (= (Personal_asentamiento As4) 4)
    (= (Suministros_almacen Al1) 1)
    (= (Suministros_almacen Al2) 0)
    (= (Suministros_almacen Al3) 0)
    (= (Entregas_restantes) 6)
)
(:goal 
    (= (Entregas_restantes) 0)
)



;un-comment the following line if metric is needed
(:metric minimize (Total_combustible_gastat))
)