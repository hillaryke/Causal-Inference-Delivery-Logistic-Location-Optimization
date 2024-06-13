# Logistic optimization: Delivery drivers location optimisation with Causal Inference

## About

The project aims to optimize the placement of Gokada's delivery drivers
(referred to as "pilots") to minimize unfulfilled delivery requests. To achieve
this, we will leverage causal inference, a statistical framework that goes
beyond correlation to uncover cause-and-effect relationships.

## Data

The project utilizes two datasets:

**Completed Orders**: This dataset provides information on successful
deliveries, including the origin, destination, and timestamps of each trip. This
data is crucial for understanding the spatial and temporal patterns of completed
deliveries, which can serve as a baseline for comparison with unfulfilled
requests.

**Delivery Requests**: This dataset includes both completed and unfulfilled
requests, along with details about the driver's location and whether they
accepted or rejected the request. This data is essential for identifying factors
that might contribute to a driver accepting or rejecting a request, such as
distance to the pickup location, time of day, or other contextual factors.

By analyzing these datasets together, we can gain insights into the factors that
influence the success or failure of a delivery. For example, we can investigate
whether drivers in certain locations are more likely to reject requests, or
whether certain times of day are associated with higher rates of unfulfilled
deliveries.

## Causal Learning

Causal learning is a critical component of this project. It involves
constructing a causal graph, a visual representation of the hypothesized causal
relationships between variables. This graph will be based on domain knowledge
and expert opinion, and it will be refined using causal discovery algorithms
applied to the observational data.

The causal graph will help us identify potential confounding variables, which
are factors that might influence both the driver's decision to accept a request
and the outcome of the delivery. By controlling for these confounders, we can
isolate the true causal effect of driver location on order fulfillment.

Once the causal graph is established, we will use do-calculus, a set of
mathematical rules for manipulating causal expressions, to estimate the causal
effects of different interventions. For example, we can simulate the effect of
relocating drivers to different areas or changing their working hours to see how
these changes would impact the number of unfulfilled requests.

## Conclusion

By combining causal inference with machine learning techniques, we can develop
predictive models that can forecast the outcome of deliveries under different
scenarios. These models can then be used to optimize driver placement and other
operational decisions, ultimately leading to a more efficient and reliable
delivery service.

#
