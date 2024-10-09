import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt

t0, t1 = 1, 1
n = 200  # 200

xt = [t0, t1]
for i in range(2, n):
    xt.append(xt[i-1] + xt[i-2])


xt_array = np.array(xt, dtype=np.float64)


log_xt = np.log(xt_array)

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(xt_array, label="X_t")
plt.title("X_t'nin Grafiği")
plt.xlabel("t")
plt.ylabel("X_t")
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(log_xt, label="log(X_t)", color='orange')
plt.title("log(X_t)'nin Grafiği")
plt.xlabel("t")
plt.ylabel("log(X_t)")
plt.legend()


plt.savefig('output_graph.png')