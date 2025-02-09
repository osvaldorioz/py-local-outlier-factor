#include <torch/torch.h>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <vector>
#include <cmath>

namespace py = pybind11;

// Calcula la distancia euclidiana entre dos puntos
double euclidean_distance(const torch::Tensor& a, const torch::Tensor& b) {
    return torch::norm(a - b, 2).item<double>();
}

// Calcula el LOF de cada punto
torch::Tensor local_outlier_factor(torch::Tensor data, int k) {
    int num_points = data.size(0);
    torch::Tensor lof_scores = torch::zeros({num_points});

    for (int i = 0; i < num_points; ++i) {
        std::vector<std::pair<double, int>> distances;
        for (int j = 0; j < num_points; ++j) {
            if (i != j) {
                distances.push_back({euclidean_distance(data[i], data[j]), j});
            }
        }

        // Ordenar por distancia y obtener los k vecinos más cercanos
        std::sort(distances.begin(), distances.end());
        std::vector<int> neighbors;
        for (int n = 0; n < k; ++n) {
            neighbors.push_back(distances[n].second);
        }

        // Calcular la densidad local
        double reachability_sum = 0.0;
        for (int n : neighbors) {
            double reach_dist = std::max(distances[n].first, euclidean_distance(data[i], data[n]));
            reachability_sum += reach_dist;
        }
        double lrd_i = k / reachability_sum;

        // Calcular LOF
        double sum_lrd_ratios = 0.0;
        for (int n : neighbors) {
            double reachability_sum_n = 0.0;
            for (int m : neighbors) {
                reachability_sum_n += std::max(distances[m].first, euclidean_distance(data[n], data[m]));
            }
            double lrd_n = k / reachability_sum_n;
            sum_lrd_ratios += lrd_n / lrd_i;
        }

        lof_scores[i] = sum_lrd_ratios / k;
    }

    return lof_scores;
}

// Exponer la función a Python
PYBIND11_MODULE(lof, m) {
    m.def("local_outlier_factor", &local_outlier_factor, "Compute LOF anomaly scores", py::arg("data"), py::arg("k") = 5);
}
