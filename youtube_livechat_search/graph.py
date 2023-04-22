import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / float(N)


def time_fmt(ens, formatter=lambda x: x.timestamp):
    times = (datetime.datetime.strptime(en.datetime, '%Y-%m-%d %H:%M:%S') for en in ens)
    if formatter is None:
        return list(times)
    else:
        return list(map(formatter, times))


def to_hist(ens):
    return np.histogram(ens, np.arange(np.floor(min(ens)), np.ceil(max(ens) + 1)))


def curve(ens, ax=None, show=True):
    raise NotImplemented
    if ax is None:
        ax = plt.gca()
    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    c, = plt.plot(time_fmt(ens))
    if not ens:
        plt.text(0.5, 0.5, 'Empty', size=72, color='r', transform=ax.transAxes, va='center', ha='center')
    plt.show()
    return c


def hist(ens, ax=None, show=True):
    if ax is None:
        ax = plt.gca()
    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    h = plt.hist(time_fmt(ens, formatter=None), histtype='stepfilled', bins='auto')
    if not ens:
        plt.text(0.5, 0.5, 'Empty', size=72, color='r', transform=ax.transAxes, va='center', ha='center')
    if show:
        plt.show()
    return h
