import simpy
import random
import Process as pro


Time_Taken = 0
Total_Time = 0
Total_Processes = 0



#Funcion New recibe un nuevo proceso y guarda en colas si no puede pasar a ready
def new(env, process):
    time = random.expovariate(1.0/10.0)
    yield env.timeout(time)
    while RAM.level < pro.Process.getRAM(process):
        left = RAM.capacity - RAM.level
        
        yield RAM.get(pro.Process.getRAM(process))
        
        
    print('%s entered the RAM at %s' % (pro.Process.getName(process), env.now))
    env.process(ready(env, process))
    yield env.timeout(1)
        
    
    


#Funcion Ready tiene espacio limitado y pasa proceso cuando se vacia el CPU (Running)
def ready(env, process):
    with CPU.request() as req:
        yield req
        print('%s entered the CPU at %s' % (pro.Process.getName(process), env.now))
        env.process(running(env, process))
        yield env.timeout(0)
        
    
    
    


#Funcion Running realiza 3 instrucciones del proceso 
def running(env, process):
    if pro.Process.getInstructions(process) < 3:     #Modificar para que el CPU procese mas de 3 isntrucciones
        pro.Process.setInstructions(process, pro.Process.getInstructions(process) - 3)
        rand = random.randint(1,2)
        if rand == 1:
            env.process(waiting(env, process))
        else:
            env.process(ready(env,process))
        yield env.timeout(1)
    else:
        env.process(terminated(env, process))
        yield env.timeout(1)
    


#Funcion Waiting hace operaciones I/O y al dejar la cola regresa a ready
def waiting(env, process):
    print('%s has done I/O operations at %s' % (pro.Process.getName(process), env.now))
    env.process(ready(env,process))
    yield env.timeout(0)
    


#Funcion Terminated hace que el proceso salga del sistema
def terminated(env, process):
    print('%s exited the CPU at %s' % (pro.Process.getName(process), env.now))
    yield env.timeout(0)


env = simpy.Environment()
RAM = simpy.Container(env, init = 100, capacity = 100)
CPU = simpy.Resource(env, capacity = 1)

random.seed(10)

for i in range(10):
    inst = 3     #Numero de instrucciones del proceso
    ram = random.randint(1, 10) #Espacio en la ram necesitado
    pr = pro.Process(i, ram, inst)
    env.process(new(env, pr))




env.run()