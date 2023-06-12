from functions_final import DeepQLearning
import gym

env=gym.make('CartPole-v1')

gamma=1
epsilon=0.1
numberEpisodes=1000

# create an object
LearningQDeep=DeepQLearning(env,gamma,epsilon,numberEpisodes)
# run the learning process
LearningQDeep.trainingEpisodes()
# get the obtained rewards in every episode
LearningQDeep.sumRewardsEpisode

#  summarize the model
LearningQDeep.mainNetwork.summary()
# save the model, this is important, since it takes long time to train the model 
# and we will need model in another file to visualize the trained model performance
LearningQDeep.mainNetwork.save("trained_model_temp.h5")



