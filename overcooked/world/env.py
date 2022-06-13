from gym.spaces import Discrete, Box
import pygame
import numpy as np
import functools
from pettingzoo import AECEnv
from pettingzoo.utils import agent_selector
from pettingzoo.utils import wrappers


from overcooked.world.world import World





ROCK = 0
PAPER = 1
SCISSORS = 2
NONE = 3
MOVES = ["ROCK", "PAPER", "SCISSORS", "None"]
NUM_ITERS = 100
REWARD_MAP = {
    (ROCK, ROCK): (0, 0),
    (ROCK, PAPER): (-1, 1),
    (ROCK, SCISSORS): (1, -1),
    (PAPER, ROCK): (1, -1),
    (PAPER, PAPER): (0, 0),
    (PAPER, SCISSORS): (-1, 1),
    (SCISSORS, ROCK): (-1, 1),
    (SCISSORS, PAPER): (1, -1),
    (SCISSORS, SCISSORS): (0, 0),
}


def overcooked_env(level_txt):
    """
    The env function often wraps the environment in wrappers by default.
    You can find full documentation for these methods
    elsewhere in the developer documentation.
    """
    env = raw_env(level_txt)
    # This wrapper is only for environments which print results to the terminal
    env = wrappers.CaptureStdoutWrapper(env)
    # this wrapper helps error handling for discrete action spaces
    env = wrappers.AssertOutOfBoundsWrapper(env)
    # Provides a wide vareity of helpful user errors
    # Strongly recommended
    env = wrappers.OrderEnforcingWrapper(env)
    return env


class raw_env(AECEnv):
    """
    The metadata holds environment constants. From gym, we inherit the "render_modes",
    metadata which specifies which modes can be put into the render() method.
    At least human mode should be supported.
    The "name" metadata allows the environment to be pretty printed.
    """

    metadata = {"render_modes": ["human"], "name": "overcooked_v0"}

    def __init__(self, level_txt):
        """
        The init method takes in environment arguments and
         should define the following attributes:
        - possible_agents
        - action_spaces
        - observation_spaces

        These attributes should not be changed after initialization.
        """

        self.world = World(level_txt)
        self.level_txt = level_txt 

        self.possible_agents = [p.name for p in self.world.players]
        self.agent_name_mapping = dict(
            zip(self.possible_agents, list(range(len(self.possible_agents))))
        )
        # Gym spaces are defined and documented here: https://gym.openai.com/docs/#spaces
        self._action_spaces = {agent: Discrete(5) for agent in self.possible_agents}

        space = Box(
                low=0,
                high=255,
                shape=(560, 560, 3),
                dtype=np.uint8,
            )

        self._observation_spaces = {
            agent: space for agent in self.possible_agents
        }

    # this cache ensures that same space object is returned for the same agent
    # allows action space seeding to work as expected
    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        # Gym spaces are defined and documented here: https://gym.openai.com/docs/#spaces
        return Box(
                low=0,
                high=255,
                shape=(560, 560, 3),
                dtype=np.uint8,
            )

    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        return Discrete(5)

    def render(self, mode="human"):
        """
        Renders the environment. In human mode, it can print to terminal, open
        up a graphical window, or open up some other display that a human can see and understand.
        """
        self.world.render()

    def observe(self, agent):
        """
        Observe should return the observation of the specified agent. This function
        should return a sane observation (though not necessarily the most up to date possible)
        at any time after reset() is called.
        """
        # observation of one agent is the previous state of the other
        return self.world.array()

    def close(self):
        """
        Close should release any graphical displays, subprocesses, network connections
        or any other environment data which should not be kept around after the
        user is no longer using the environment.
        """
        pygame.quit()

    def reset(self, seed=None):
        """
        Reset needs to initialize the following attributes
        - agents
        - rewards
        - _cumulative_rewards
        - dones
        - infos
        - agent_selection
        And must set up the environment so that render(), step(), and observe()
        can be called without issues.

        Here it sets up the state dictionary which is used by step() and the observations dictionary which is used by step() and observe()
        """
        self.world = World(self.level_txt)

        self.agents = self.possible_agents[:]
        self.rewards = {agent: 0 for agent in self.agents}
        self._cumulative_rewards = {agent: 0 for agent in self.agents}
        self.dones = {agent: False for agent in self.agents}
        self.infos = {agent: {} for agent in self.agents}
        self.state = {agent: None for agent in self.agents}
        self.observations = {agent: None for agent in self.agents}
        self.num_moves = 0
        """
        Our agent_selector utility allows easy cyclic stepping through the agents list.
        """
        self._agent_selector = agent_selector(self.agents)
        self.agent_selection = self._agent_selector.next()

    def step(self, action):
        """
        step(action) takes in an action for the current agent (specified by
        agent_selection) and needs to update
        - rewards
        - _cumulative_rewards (accumulating the rewards)
        - dones
        - infos
        - agent_selection (to the next agent)
        And any internal state used by observe() or render()
        """
        if self.dones[self.agent_selection]:
            # handles stepping an agent which is already done
            # accepts a None action for the one agent, and moves the agent_selection to
            # the next done agent,  or if there are no more done agents, to the next live agent
            return self._was_done_step(action)

        agent = self.agent_selection

        # the agent which stepped last had its _cumulative_rewards accounted for
        # (because it was returned by last()), so the _cumulative_rewards for this
        # agent should start again at 0
        self._cumulative_rewards[agent] = 0

        # stores action of current agent
        self.state[self.agent_selection] = action

        reward, done = self.world.execute_action(self.agent_selection, action)
        self.rewards[self.agent_selection] = reward
        self.dones[self.agent_selection] = done


        # collect reward if it is the last agent to act
        if self._agent_selector.is_last():
            # rewards for all agents are placed in the .rewards dictionary
            self.num_moves += 1

        else:
            self._clear_rewards()

        # selects the next agent.
        self.agent_selection = self._agent_selector.next()
        # Adds .rewards to ._cumulative_rewards
        self._accumulate_rewards()