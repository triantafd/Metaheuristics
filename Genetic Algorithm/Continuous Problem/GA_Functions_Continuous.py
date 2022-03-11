###################################################################
### FOR THE HIMMELBLAU FUNCTION
### FUNCTION DEFINITIONS
### GENETIC ALGORITHM OPERATORS
### DECODING / OBJ. VAL. / PARENT SELECTION / CROSSOVER / MUTATION 
###################################################################
### Owner: Dana Bani-Hani
### Copyright © 2019 Curiosity for Data Science
###################################################################


import numpy as np


################################################
### CALCULATING THE OBJECTIVE FUNCTION VALUE ###
################################################

# calculate fitness value for the chromosome of 0s and 1s
def objective_value(chromosome):  
    
    lb_x = -6 # lower bound for chromosome x
    ub_x = 6 # upper bound for chromosome x
    len_x = (len(chromosome)//2) # length of chromosome x
    lb_y = -6 # lower bound for chromosome y
    ub_y = 6 # upper bound for chromosome y
    len_y = (len(chromosome)//2) # length of chromosome y
    
    precision_x = (ub_x-lb_x)/((2**len_x)-1) # precision for decoding x
    precision_y = (ub_y-lb_y)/((2**len_y)-1) # precision for decoding y
    
    z = 0 # because we start at 2^0, in the formula
    t = 1 # because we start at the very last element of the vector [index -1]
    x_bit_sum = 0 # initiation (sum(bit)*2^i is 0 at first)
    for i in range(len(chromosome)//2):
        x_bit = chromosome[-t]*(2**z)
        x_bit_sum = x_bit_sum + x_bit
        t = t+1
        z = z+1   
    
    z = 0 # because we start at 2^0, in the formula
    t = 1 + (len(chromosome)//2) # [6,8,3,9] (first 2 are y, so index will be 1+2 = -3)
    y_bit_sum = 0 # initiation (sum(bit)*2^i is 0 at first)
    for j in range(len(chromosome)//2):
        y_bit = chromosome[-t]*(2**z)
        y_bit_sum = y_bit_sum + y_bit
        t = t+1
        z = z+1
    
    # the formulas to decode the chromosome of 0s and 1s to an actual number, the value of x or y
    decoded_x = (x_bit_sum*precision_x)+lb_x
    decoded_y = (y_bit_sum*precision_y)+lb_y
    
    # the himmelblau function
    # min ((x**2)+y-11)**2+(x+(y**2)-7)**2
    # objective function value for the decoded x and decoded y
    obj_function_value = ((decoded_x**2)+decoded_y-11)**2+(decoded_x+(decoded_y**2)-7)**2
    
    return decoded_x,decoded_y,obj_function_value # the defined function will return 3 values



#################################################
### SELECTING TWO PARENTS FROM THE POPULATION ###
### USING TOURNAMENT SELECTION METHOD ###########
#################################################

# finding 2 parents from the pool of solutions
# using the tournament selection method 
def find_parents_ts(all_solutions):
    
    # make an empty array to place the selected parents
    parents = np.empty((0,np.size(all_solutions,1)))
    
    for i in range(2): # do the process twice to get 2 parents
        
        # select 3 random parents from the pool of solutions you have
        
        # get 3 random integers
        indices_list = np.random.choice(len(all_solutions),3,replace=False)
        
        # get the 3 possible parents for selection
        posb_parent_1 = all_solutions[indices_list[0]]
        posb_parent_2 = all_solutions[indices_list[1]]
        posb_parent_3 = all_solutions[indices_list[2]]
        
        # get objective function value (fitness) for each possible parent
        # index no.2 because the objective_value function gives the fitness value at index no.2
        obj_func_parent_1 = objective_value(posb_parent_1)[2] # possible parent 1
        obj_func_parent_2 = objective_value(posb_parent_2)[2] # possible parent 2
        obj_func_parent_3 = objective_value(posb_parent_3)[2] # possible parent 3
        
        # find which parent is the best
        min_obj_func = min(obj_func_parent_1,obj_func_parent_2,obj_func_parent_3)
        
        if min_obj_func == obj_func_parent_1:
            selected_parent = posb_parent_1
        elif min_obj_func == obj_func_parent_2:
            selected_parent = posb_parent_2
        else:
            selected_parent = posb_parent_3
        
        # put the selected parent in the empty array we created above
        parents = np.vstack((parents,selected_parent))
        
    parent_1 = parents[0,:] # parent_1, first element in the array
    parent_2 = parents[1,:] # parent_2, second element in the array
    
    return parent_1,parent_2 # the defined function will return 2 arrays



####################################################
### CROSSOVER THE TWO PARENTS TO CREATE CHILDREN ###
####################################################

# crossover between the 2 parents to create 2 children
# functions inputs are parent_1, parent_2, and the probability you would like for crossover
# default probability of crossover is 1
def crossover(parent_1,parent_2,prob_crsvr=1):
    
    child_1 = np.empty((0,len(parent_1)))
    child_2 = np.empty((0,len(parent_2)))
    
    
    rand_num_to_crsvr_or_not = np.random.rand() # do we crossover or no???
    
    if rand_num_to_crsvr_or_not < prob_crsvr:
        index_1 = np.random.randint(0,len(parent_1))
        index_2 = np.random.randint(0,len(parent_2))
        
        # get different indices
        # to make sure you will crossover at least one gene
        while index_1 == index_2:
            index_2 = np.random.randint(0,len(parent_1))
        
        
        # IF THE INDEX FROM PARENT_1 COMES BEFORE PARENT_2
        # e.g. parent_1 = 0,1,>>1<<,1,0,0,1,0 --> index = 2
        # e.g. parent_2 = 0,0,1,0,0,1,>>1<<,1 --> index = 6
        if index_1 < index_2:
            
            
            ### FOR PARENT_1 ###
            ### FOR PARENT_1 ###
            ### FOR PARENT_1 ###
            
            # first_seg_parent_1 -->
            # for parent_1: the genes from the beginning of parent_1 to the
                    # beginning of the middle segment of parent_1
            first_seg_parent_1 = parent_1[:index_1]
            
            # middle segment; where the crossover will happen
            # for parent_1: the genes from the index chosen for parent_1 to
                    # the index chosen for parent_2
            mid_seg_parent_1 = parent_1[index_1:index_2+1]
            
            # last_seg_parent_1 -->
            # for parent_1: the genes from the end of the middle segment of
                    # parent_1 to the last gene of parent_1
            last_seg_parent_1 = parent_1[index_2+1:]
            
            
            ### FOR PARENT_2 ###
            ### FOR PARENT_2 ###
            ### FOR PARENT_2 ###
            
            # first_seg_parent_2 --> same as parent_1
            first_seg_parent_2 = parent_2[:index_1]
            
            # mid_seg_parent_2 --> same as parent_1
            mid_seg_parent_2 = parent_2[index_1:index_2+1]
            
            # last_seg_parent_2 --> same as parent_1
            last_seg_parent_2 = parent_2[index_2+1:]
            
            
            ### CREATING CHILD_1 ###
            ### CREATING CHILD_1 ###
            ### CREATING CHILD_1 ###
            
            # the first segmant from parent_1
            # plus the middle segment from parent_2
            # plus the last segment from parent_1
            child_1 = np.concatenate((first_seg_parent_1,mid_seg_parent_2,
                                      last_seg_parent_1))
            
            
            ### CREATING CHILD_2 ###
            ### CREATING CHILD_2 ###
            ### CREATING CHILD_2 ###
            
            # the first segmant from parent_2
            # plus the middle segment from parent_1
            # plus the last segment from parent_2
            child_2 = np.concatenate((first_seg_parent_2,mid_seg_parent_1,
                                      last_seg_parent_2))
        
        
        
        ### THE SAME PROCESS BUT INDEX FROM PARENT_2 COMES BEFORE PARENT_1
        # e.g. parent_1 = 0,0,1,0,0,1,>>1<<,1 --> index = 6
        # e.g. parent_2 = 0,1,>>1<<,1,0,0,1,0 --> index = 2
        else:
            
            first_seg_parent_1 = parent_1[:index_2]
            mid_seg_parent_1 = parent_1[index_2:index_1+1]
            last_seg_parent_1 = parent_1[index_1+1:]
            
            first_seg_parent_2 = parent_2[:index_2]
            mid_seg_parent_2 = parent_2[index_2:index_1+1]
            last_seg_parent_2 = parent_2[index_1+1:]
            
            
            child_1 = np.concatenate((first_seg_parent_1,mid_seg_parent_2,
                                      last_seg_parent_1))
            child_2 = np.concatenate((first_seg_parent_2,mid_seg_parent_1,
                                      last_seg_parent_2))
     
    # when we will not crossover
    # when rand_num_to_crsvr_or_not is NOT less (is greater) than prob_crsvr
    # when prob_crsvr == 1, then rand_num_to_crsvr_or_not will always be less
            # than prob_crsvr, so we will always crossover then
    else:
        child_1 = parent_1
        child_2 = parent_2
    
    return child_1,child_2 # the defined function will return 2 arrays



############################################################
### MUTATING THE TWO CHILDREN TO CREATE MUTATED CHILDREN ###
############################################################

# mutation for the 2 children
# functions inputs are child_1, child_2, and the probability you would like for mutation
# default probability of mutation is 0.2
def mutation(child_1,child_2,prob_mutation=0.2):
    
    # mutated_child_1
    mutated_child_1 = np.empty((0,len(child_1)))
      
    t = 0 # start at the very first index of child_1
    for i in child_1: # for each gene (index)
        
        rand_num_to_mutate_or_not_1 = np.random.rand() # do we mutate or no???
        
        # if the rand_num_to_mutate_or_not_1 is less that the probability of mutation
                # then we mutate at that given gene (index we are currently at)
        if rand_num_to_mutate_or_not_1 < prob_mutation:
            
            if child_1[t] == 0: # if we mutate, a 0 becomes a 1
                child_1[t] = 1
            
            else:
                child_1[t] = 0  # if we mutate, a 1 becomes a 0
            
            mutated_child_1 = child_1
            
            t = t+1
        
        else:
            mutated_child_1 = child_1
            
            t = t+1
    
       
    # mutated_child_2
    # same process as mutated_child_1
    mutated_child_2 = np.empty((0,len(child_2)))
    
    t = 0
    for i in child_2:
        
        rand_num_to_mutate_or_not_2 = np.random.rand() # prob. to mutate
        
        if rand_num_to_mutate_or_not_2 < prob_mutation:
            
            if child_2[t] == 0:
                child_2[t] = 1
           
            else:
                child_2[t] = 0
            
            mutated_child_2 = child_2
            
            t = t+1
        
        else:
            mutated_child_2 = child_2
            
            t = t+1
    
    return mutated_child_1,mutated_child_2 # the defined function will return 2 arrays




