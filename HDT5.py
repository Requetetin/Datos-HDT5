#Martín Amado Girón
#19020
#Hoja de trabajo numero 5
#Algoritmos y estructuras de datos

import simpy
import random
import Process as pro


Time_Taken = 0
Total_Time = 0



#Funcion New recibe un nuevo proceso y guarda en colas si no puede pasar a ready
def new(env, process):
    time = random.expovariate(1.0/10.0)
    yield env.timeout(time)
    while RAM.level < pro.Process.getRAM(process):
        left = RAM.capacity - RAM.level
        
        yield RAM.get(pro.Process.getRAM(process))
        
        
    print('%s entered the RAM at %.2f' % (pro.Process.getName(process), env.now))
    pro.Process.setInicio(process, env.now)
    yield env.timeout(1)
    env.process(ready(env, process))
    
        
    
    


#Funcion Ready tiene espacio limitado y pasa proceso cuando se vacia el CPU (Running)
def ready(env, process):
    with CPU.request() as req:
        yield req
        print('%s entered the CPU at %.2f' % (pro.Process.getName(process), env.now))
        env.process(running(env, process))
        yield env.timeout(0)
        
    
    
    


#Funcion Running realiza 3 instrucciones del proceso 
def running(env, process):
    if pro.Process.getInstructions(process) > 5:     #Modificar para que el CPU procese mas de 3 isntrucciones
        pro.Process.setInstructions(process, pro.Process.getInstructions(process) - 3)
        rand = random.randint(1,2)
        if rand == 1:
            env.process(waiting(env, process))
        else:
            yield env.timeout(1)
            env.process(ready(env,process))
    else:
        yield env.timeout(1)
        env.process(terminated(env, process))
    


#Funcion Waiting hace operaciones I/O y al dejar la cola regresa a ready
def waiting(env, process):
    print('%s has done I/O operations and entered the RAM at %.2f' % (pro.Process.getName(process), env.now))
    env.process(ready(env,process))
    yield env.timeout(0)
    


#Funcion Terminated hace que el proceso salga del sistema
def terminated(env, process):
    print('%s exited the CPU at %.2f' % (pro.Process.getName(process), env.now))
    global Total_Time
    Total_Time = env.now
    pro.Process.setFinal(process, env.now)
    yield env.timeout(0)


env = simpy.Environment()
RAM = simpy.Container(env, init = 200, capacity = 200)  #Cambiar para RAM
CPU = simpy.Resource(env, capacity = 2) #Cambiar CPU

random.seed(10)
Corridas = 200  #Cambiar para el numero de procesos
procesos = list()
for i in range(Corridas):
    inst = random.randint(1,10)     #Numero de instrucciones del proceso
    ram = random.randint(1, 10) #Espacio en la ram necesitado
    pr = pro.Process(i, ram, inst)
    procesos.append(pr)
    env.process(new(env, pr))




env.run()
print('')
print('El promedio de corrida fue de: %.2f' % (Total_Time/Corridas)) 
Media = Total_Time/Corridas
s = 0
for i in procesos:
    s += (i.getTime()-Media)**2

Desvest = (s/Corridas)**(1/2.0)
print('La desviacion estandar de la corrida fue de: %.2f' % (Desvest))


