import numpy as np
import matplotlib.pyplot as plt
import os
import platform

from IPython.display import display, Markdown, Latex
from matplotlib.widgets import Slider

from sklearn.preprocessing import StandardScaler

__version__ = '0.2.5'

class Exercise1Utils:
    def load_npy(file_name):
        data_path = os.path.join(os.path.dirname(__file__), 'datasets', 'exercise1', file_name)
        return np.load(data_path)

    @staticmethod
    def load_data_exercise_1():
        train_data = Exercise1Utils.load_npy('train_data.npy')
        train_labels = Exercise1Utils.load_npy('train_labels.npy')
        test_data = Exercise1Utils.load_npy('test_data.npy')
        test_labels = Exercise1Utils.load_npy('test_labels.npy')
            
        return train_data, train_labels, test_data, test_labels

class Exercise2Utils:
    @staticmethod
    def load_data_exercise_2():
        data_path = os.path.join(os.path.dirname(__file__), 'datasets', 'exercise2', 'ex1data2.txt')
        data = np.loadtxt(data_path, delimiter=',', dtype=np.float64)
        x = data[:, :1] / 100 # We will only use the size as a feature
        y = data[:, 2] / 1000 # convert to 1000$
        m = y.size
        return x, y, m

    @staticmethod
    def plotData(x_train, y_train, x_test, y_test):
        plt.figure(figsize=(10,5))
        plt.scatter(x_train, y_train, label='train data')
        plt.scatter(x_test, y_test, label='test data')
        plt.ylabel('Price in 1000$')
        plt.xlabel('Size in 100 sq-feet')
        plt.legend(loc=4)

    @staticmethod
    def plotLine(x_train, y_train, x_test, y_test, w):
        Exercise2Utils.plotData(x_train, y_train, x_test, y_test)

        # Regression Line
        axes = plt.gca()
        x_vals = np.array(axes.get_xlim())
        y_vals = w[0] + w[1] * x_vals
        plt.plot(x_vals, y_vals, '-')

    @staticmethod
    def plotPolyLine(x_train, y_train, x_test, y_test, w):
        Exercise2Utils.plotData(x_train, y_train, x_test, y_test)

        # Regression Line
        axes = plt.gca()
        x_vals = np.array(axes.get_xlim())
        y_vals = w[0] + w[1] * x_vals
        plt.plot(x_vals, y_vals, '-')

        # Regression Polynom
        X_poly = mapPolynomialFeatures(x[:, 0], np.ones(len(x[:, 0])), 3)
        w_poly = normalEqn(X_poly, y);
        x1 = np.float32(np.linspace(500, 4500, 1000))
        x2 = np.float32(np.linspace(1, 1, 1000))
        polys = mapPolynomialFeatures(x1, x2, 3)

        y_vals = predictPrice(polys, w_poly)
        plt.plot(x1, y_vals, '.')

    @staticmethod
    def plotLossFunction(X, y, w0_vals, w1_vals, L_vals, w):
        # surface plot
        fig = plt.figure(figsize=(12, 5))
        ax = fig.add_subplot(121, projection='3d')
        ax.plot_surface(w0_vals, w1_vals, L_vals, cmap='viridis')
        plt.xlabel('w0')
        plt.ylabel('w1')
        plt.title('Surface')

        # contour plot
        ax = plt.subplot(122)
        plt.contour(w0_vals, w1_vals, L_vals, linewidths=2, levels=20)
        plt.xlabel('w0')
        plt.ylabel('w1')
        plt.plot(w[0], w[1], 'ro', ms=10, lw=2)
        plt.title('Contour, showing minimum')

    @staticmethod
    def plot_one(X_train, y_train, X_test, y_test, degree_predictions, x_interval, degree):
        plt.figure(figsize=(10,5))
        plt.plot(X_train, y_train, 'o', label='training data', markersize=10)
        plt.plot(X_test, y_test, 'o', label='test data', markersize=10)
        for i,degree in enumerate(degree):
            plt.plot(x_interval, degree_predictions[i],
                     alpha=0.8, lw=2, label='degree={}'.format(degree))
        plt.legend(loc=4)
        plt.ylim(0,1000)
        plt.xlim(0,60)

    @staticmethod
    def plot_validation_curve(mse_train, mse_test, degrees):
        plt.figure(figsize=(14,5))
        plt.title('Validation Curve')
        plt.xlabel('poly')
        plt.ylabel('RMSE')
        plt.ylim(20, 100)
        plt.xticks(np.arange(min(degrees), max(degrees)+1, 1.0))

        plt.plot(degrees, np.sqrt(mse_train), label='Training MSE', color='darkorange', lw=2)
        plt.plot(degrees, np.sqrt(mse_test), label='Test MSE', color='navy', lw=2)
        plt.legend(loc='best')
        plt.show()

    @staticmethod
    def plot_polynomial_rmse(polys, Ls_poly_train):
        plt.figure(figsize=(8,5))  
        plt.plot(polys, Ls_poly_train, '-', label="RMSE")
        plt.xlabel('polynomial degree')
        plt.ylabel('RMSE')
        plt.title('RMSE for varying polynomial degrees')
        _ = plt.legend(loc='best')

class Exercise3Utils:
    @staticmethod
    def load_exam_data():
        # The first two columns contains the exam scores and the third column
        # contains the label.
        data_path = os.path.join(os.path.dirname(__file__), 'datasets', 'exercise3', 'ex2data1.txt')
        data = np.loadtxt(data_path, delimiter=',', dtype=np.float64)
        X, y = data[:, 0:2], data[:, 2]
        
        # we norm the data
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
        
        return X, y, scaler

    @staticmethod
    def load_microchip_data():
        data_path = os.path.join(os.path.dirname(__file__), 'datasets', 'exercise3', 'ex2data2.txt')
        data = np.loadtxt(data_path, delimiter=',', dtype=np.float64)
        X = data[:, :2]
        y = data[:, 2]
        
        # we norm the data
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
        
        return X, y, scaler


    @staticmethod
    def load_sentiment_data():
        data_path = os.path.join(os.path.dirname(__file__), 'datasets', 'exercise3', 'full_set.txt')
        content = np.loadtxt(data_path, dtype=object, delimiter="\t")
        
        ## Separate the sentences from the labels
        sentences = np.array([x[0].strip() for x in content])
        labels = np.array([x[1].strip() for x in content])

        ## Transform the labels from '0 v.s. 1' to '-1 v.s. 1'
        y = np.array(labels, dtype='int8')
        y = 2*y - 1
        
        return sentences, labels, y


    @staticmethod
    def plotData(X, y):
        fig = plt.figure(figsize=(12,8))

        # Find Indices of Positive and Negative Examples
        pos = y == 1
        neg = y == 0

        # Plot Examples
        plt.plot(X[pos, 0], X[pos, 1], 'x', lw=2, ms=10)
        plt.plot(X[neg, 0], X[neg, 1], 'o', ms=10)

        plt.xlabel('Normalized Exam 1 score')
        plt.ylabel('Normalized Exam 2 score')

        plt.legend(['Admitted', 'Not admitted'])

    @staticmethod   
    def mapFeature(X1, X2, degree=6):
        if X1.ndim > 0:
            out = [np.ones(X1.shape[0], dtype=np.float64)]
        else:
            # out = [np.ones(1, dtype=np.float64)]
            out = [1]

        for i in range(1, degree + 1):
            for j in range(i + 1):
                out.append((X1 ** (i - j)) * (X2 ** j))

        if X1.ndim > 0:
            return np.stack(out, axis=1, dtype=np.float64)
        else:
            return np.array(out, dtype=np.float64)

    @staticmethod
    def plotDecisionBoundary(plotData, theta, X, y, degree=6):
        # make sure theta is a numpy array
        theta = np.array(theta)

        # Plot Data (remember first column in X is the intercept)
        plotData(X[:, 1:3], y)

        if X.shape[1] <= 3:
            # Only need 2 points to define a line, so choose two endpoints
            plot_x = np.array([np.min(X[:, 1]), np.max(X[:, 1])])

            # Calculate the decision boundary line
            plot_y = (-1. / theta[2]) * (theta[1] * plot_x + theta[0])

            # Plot, and adjust axes for better viewing
            plt.plot(plot_x, plot_y)

            # Legend, specific for the exercise
            plt.legend(['Admitted', 'Not admitted', 'Decision Boundary'])
            #plt.xlim([1, 100])
            #plt.ylim([1, 100])
        else:
            # Here is the grid range
            u = np.linspace(-2, 2, 50)
            v = np.linspace(-2, 2, 50)

            z = np.zeros((u.size, v.size))
            # Evaluate z = theta*x over the grid
            for i, ui in enumerate(u):
                for j, vj in enumerate(v):
                    z[i, j] = np.dot(Exercise3Utils.mapFeature(ui, vj, degree), theta)

            z = z.T  # important to transpose z before calling contour

            plt.contour(u, v, z, levels=[0], linewidths=2, colors='g')

        plt.tight_layout()

    @staticmethod
    def vis_coef(estimator, feature_names, topn = 10):
        """
        Visualize the top-n most influential coefficients
        for linear models.
        """
        fig = plt.figure(figsize=(10,15))
        feature_names = np.array(feature_names)

        coefs  = estimator.coef_[0]
        sorted_coefs = np.argsort(coefs)
        positive_coefs = sorted_coefs[-topn:]
        negative_coefs = sorted_coefs[:topn]

        top_coefs = np.hstack([negative_coefs, positive_coefs])
        colors = ['r' if c < 0 else 'b' for c in coefs[top_coefs]]
        y_pos = np.arange(2 * topn)
        plt.barh(y_pos, coefs[top_coefs], color = colors, align = 'center')
        plt.yticks(y_pos, feature_names[top_coefs])
        plt.title('top {} positive/negative words'.format(topn))

        plt.tight_layout()


class Exercise4Utils:

    @staticmethod
    def load_data(name):
        # Load data
        data_path = os.path.join(os.path.dirname(__file__), 'datasets', 'exercise4', name)
        return np.loadtxt(data_path, dtype=np.float64)


    @staticmethod
    def plotData(X, y, grid=False):
        # Find Indices of Positive and Negative Examples
        pos = y == 1
        neg = y == 0

        # Plot Examples
        plt.plot(X[pos, 0], X[pos, 1], 'X', mew=1, ms=10, mec='k')
        plt.plot(X[neg, 0], X[neg, 1], 'o', mew=1, mfc='y', ms=10, mec='k')
        plt.grid(grid)


    @staticmethod
    def plotMargin(x, y, w, converged, predict) :
        # Determine the x1- and x2- limits of the plot
        x1min = min(x[:,0]) - 0.5
        x1max = max(x[:,0]) + 0.5
        x2min = min(x[:,1]) - 0.5
        x2max = max(x[:,1]) + 0.5
        
        plt.xlim(x1min,x1max)
        plt.ylim(x2min,x2max)
        
        # Plot the data points
        plt.plot(x[(y==1),0], x[(y==1),1], 'ro')
        plt.plot(x[(y==-1),0], x[(y==-1),1], 'k^')
        # Construct a grid of points at which to evaluate the classifier
        if converged:
            grid_spacing = 0.02
            xx1, xx2 = np.meshgrid(np.arange(x1min, x1max, grid_spacing), np.arange(x2min, x2max, grid_spacing))
            grid = np.c_[xx1.ravel(), xx2.ravel()]

            Grid = np.concatenate([np.ones((grid.shape[0], 1)), grid], axis=1)        
            Z = np.array([predict(w,pt) for pt in Grid])
            print (Z)
            
            # Show the classifier's boundary using a color plot
            Z = Z.reshape(xx1.shape)
            plt.pcolormesh(xx1, xx2, Z, shading='auto', 
                            cmap=plt.cm.PRGn, vmin=-3, vmax=3)
        
    @staticmethod 
    def display_data_and_boundary(x, y, w, predictMultiClass):
        
        #fig = plt.figure(figsize=(6,6))
        
        # Determine the x1- and x2- limits of the plot
        x1min = min(x[:,0]) - 1
        x1max = max(x[:,0]) + 1
        x2min = min(x[:,1]) - 1
        x2max = max(x[:,1]) + 1
        plt.xlim(x1min,x1max)
        plt.ylim(x2min,x2max)

        # Plot the data points
        k = int(max(y)) + 1
        cols = ['ro', 'k^', 'b*','gx']
        for label in range(k):
            plt.plot(x[(y==label),0], x[(y==label),1], cols[label%4], markersize=8)
        
        # Construct a grid of points at which to evaluate the classifier
        grid_spacing = 0.05
        xx1, xx2 = np.meshgrid(np.arange(x1min, x1max, grid_spacing), np.arange(x2min, x2max, grid_spacing))
        grid = np.c_[xx1.ravel(), xx2.ravel()]
        
        Grid = np.concatenate([np.ones((grid.shape[0], 1)), grid], axis=1)        
        Z = np.array([predictMultiClass(w,pt) for pt in Grid])    
        #Z = np.array([predictMultiClass(w, pt) for pt in grid])
        
        # Show the classifier's boundary using a color plot
        Z = Z.reshape(xx1.shape)
        plt.pcolormesh(xx1, xx2, Z, shading='auto', 
            cmap=plt.cm.Pastel1, vmin=0, vmax=k)
        plt.show()

    @staticmethod
    def visualizeBoundary(X, y, clf):
        #fig = plt.figure(figsize=(6,6))
        Exercise4Utils.plotData(X, y)

        h = .01  # step size in the mesh

        # create a mesh to plot in
        x_min, x_max = X[:, 0].min()-h, X[:, 0].max()+h
        y_min, y_max = X[:, 1].min()-h, X[:, 1].max()+h
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

        Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

        # Put the result into a color plot
        Z = Z.reshape(xx.shape)
        plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8)
        
        # Plot also the training points
        plt.scatter(X[:, 0], X[:, 1], color="g", s=3)

        plt.show()

    @staticmethod
    def visualizeBoundaryLinear(X, y, clf) :
        #fig = plt.figure(figsize=(6,6))
        Exercise4Utils.plotData(X, y)
        
        # step size in the mesh
        h = .01

        # create a mesh to plot in
        x_min, x_max = X[:, 0].min()-h, X[:, 0].max()+h
        y_min, y_max = X[:, 1].min()-h, X[:, 1].max()+h
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

        Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

        # Put the result into a color plot
        Z = Z.reshape(xx.shape)
        plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8)
        plt.axis('off')

        # Plot also the training points
        color_map = {-1: (1, 1, 1), 0: (0, 0, 0.9), 1: (1, 0, 0), 2: (0.8, 0.6, 0)}
        colors = [color_map[y] for y in y]
        plt.scatter(X[:, 0], X[:, 1], c=colors, edgecolors='black')
        plt.show()


class Exercise5Utils:

    @staticmethod
    def plot_images(X, y):
        fig, axes = plt.subplots(8, 8, figsize=(5,5))
        fig.tight_layout(pad=0.13,rect=[0, 0.03, 1, 0.91]) #[left, bottom, right, top]
        m, n = X.shape

        for i,ax in enumerate(axes.flat):
            # Select random indices
            random_index = np.random.randint(m)
            
            # Select rows corresponding to the random indices and
            # reshape the image
            X_random_reshaped = X[random_index].reshape((28,28))
            
            # Display the image
            ax.imshow(X_random_reshaped, cmap='gray')
            
            # Display the label above the image
            ax.set_title(np.int32(y[random_index]))
            ax.set_axis_off()
            fig.suptitle("Label", fontsize=14)


    @staticmethod    
    def plot_non_linear_decision_boundary(X, y, model, title="Decision Boundary"):
        Exercise3Utils.plotData(X, y)
        
        h = .02  # Step size in the mesh
        x_min, x_max = X[:, 0].min() - 0.1, X[:, 0].max() + 0.1
        y_min, y_max = X[:, 1].min() - 0.1, X[:, 1].max() + 0.1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
        
        # Make predictions on the meshgrid points
        Z = model.predict(np.c_[xx.ravel(), yy.ravel()], verbose=0)
        Z = Z.reshape(xx.shape)
        
        # Plot the contour plot
        plt.contourf(xx, yy, Z, cmap=plt.cm.RdBu, alpha=0.5)
                
        plt.show()      


    @staticmethod    
    def plt_softmax(my_softmax):
        fig, ax = plt.subplots(1,2,figsize=(8,4))
        plt.subplots_adjust(bottom=0.35)

        axz0 = fig.add_axes([0.15, 0.10, 0.30, 0.03]) # [left, bottom, width, height]
        axz1 = fig.add_axes([0.15, 0.15, 0.30, 0.03])
        axz2 = fig.add_axes([0.15, 0.20, 0.30, 0.03])
        axz3 = fig.add_axes([0.15, 0.25, 0.30, 0.03])

        z3 = Slider(axz3, 'z3', 0.1, 10.0, valinit=4, valstep=0.1)
        z2 = Slider(axz2, 'z2', 0.1, 10.0, valinit=3, valstep=0.1)
        z1 = Slider(axz1, 'z1', 0.1, 10.0, valinit=2, valstep=0.1)
        z0 = Slider(axz0, 'z0', 0.1, 10.0, valinit=1, valstep=0.1)

        z = np.array(['z0','z1','z2','z3'])
        bar = ax[0].barh(z, height=0.6, width=[z0.val,z1.val,z2.val,z3.val], left=None, align='center')
        bars = bar.get_children()
        ax[0].set_xlim([0,10])
        ax[0].set_title("z input to softmax")

        a = my_softmax(np.array([z0.val,z1.val,z2.val,z3.val]))
        anames = np.array(['a0','a1','a2','a3'])
        sbar = ax[1].barh(anames, height=0.6, width=a, left=None, align='center',color="#C00000")
        sbars = sbar.get_children()
        ax[1].set_xlim([0,1])
        ax[1].set_title("softmax(z)")

        def update(val):
            bars[0].set_width(z0.val)
            bars[1].set_width(z1.val)
            bars[2].set_width(z2.val)
            bars[3].set_width(z3.val)
            a = my_softmax(np.array([z0.val,z1.val,z2.val,z3.val]))
            sbars[0].set_width(a[0])
            sbars[1].set_width(a[1])
            sbars[2].set_width(a[2])
            sbars[3].set_width(a[3])

            fig.canvas.draw_idle()

        z0.on_changed(update)
        z1.on_changed(update)
        z2.on_changed(update)
        z3.on_changed(update)

    @staticmethod
    def display_images(X_all):
        """
        Displays 2D data stored in X in a nice grid.
        """
        # Randomly select 100 data points to display
        rand_indices = np.random.choice(X_all.shape[0], 100, replace=False)
        X = X_all[rand_indices, :]
        
        # Compute rows, cols
        if X.ndim == 2:
            m, n = X.shape
        elif X.ndim == 1:
            n = X.size
            m = 1
            X = X[None]  # Promote to a 2 dimensional array
        else:
            raise IndexError('Input X should be 1 or 2 dimensional.')

        example_width = int(np.round(np.sqrt(n)))
        example_height = n / example_width

        # Compute number of items to display
        display_rows = int(np.floor(np.sqrt(m)))
        display_cols = int(np.ceil(m / display_rows))

        fig, ax_array = plt.subplots(display_rows, display_cols, figsize=(10, 10))
        # fig.subplots_adjust(wspace=0.025, hspace=0.025)

        ax_array = [ax_array] if m == 1 else ax_array.ravel()

        for i, ax in enumerate(ax_array):
            ax.imshow(X[i].reshape(
                example_width, 
                example_width),
                cmap='Greys', extent=[0, 1, 0, 1])
            ax.axis('off') 


    def load_weights_task1():
        data_path = os.path.join(os.path.dirname(__file__), 'datasets', 'exercise5', 'weights.npz')
        weights = np.load(data_path, allow_pickle = True)
        W1 = weights["W1"]
        b1 = weights["b1"]
        W2 = weights["W2"]
        b2 = weights["b2"]   
        return W1, b1, W2, b2