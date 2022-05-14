from hmmlearn import hmm
import numpy as np
# --------------------------------------------------
# Define a class to train the HMM
class ModelHMM(object):
    """
    Class for Hidden Markov Model.
    This class defines methods for training and compute score
    """
    def __init__(self, num_components=4, num_iter=1000):
        """
        Initialize params for hmm
        :param num_components:
        :param num_iter:
        """
        self.n_components = num_components
        self.n_iter = num_iter

        self.cov_type = 'diag'
        self.model_name = 'GaussianHMM'

        self.models = []
        self.model = hmm.GaussianHMM(n_components=self.n_components, covariance_type=self.cov_type, n_iter=self.n_iter)

        self.speech_models = []
        # ----------------------------------

    # 'training_data' is a 2D numpy array where each row is 13-dimensional
    def train(self, training_data):
        np.seterr(all='ignore')
        cur_model = self.model.fit(training_data)
        self.models.append(cur_model)

    # Run the HMM model for inference on input data
    def compute_score(self, input_data):
        return self.model.score(input_data)
# ------------------------------------------------
