#!/usr/bin/env python

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.ticker import MaxNLocator
from parse import parse_file

def plot_pilotlifetime(pilot_lifetimes, cus, tq, ltf):

    # Pilot Life times
    pilot_start_times = []
    durations = []
    cum_cores = 0
    pilots = []
    for cores, new, running, end in pilot_lifetimes:
        if not end:
            end = ltf + 1
        pilot_start_times.append(new) # collect start coordinates
        durations.append(end-new) # collect duration
        y = cum_cores + cores/2.0 + 0.5
        pilots.append(y)
        cum_cores += cores
    pilot_durations = [ [0] * len(pilots), durations ] # error = [(0, duration)]

    eb = plt.subplot(111)
    eb.yaxis.set_major_locator(MaxNLocator(integer=True))
    eb.set_ylabel('ComputePilot Instance')
    eb.set_xlabel('Time (s)')
    eb.set_ylim(0,10)

    # Plot total lifetime
    eb.errorbar(pilot_start_times, pilots, xerr=pilot_durations, fmt='None', ecolor='black', label='ComputePilot')

    # Pilot Queue times
    color='red'
    cum_cores = 0
    for cores, new, running, end in pilot_lifetimes:
        y = cum_cores + cores/2.0 + 0.5
        #y = cum_cores + cores
        #y = cum_cores + cores/2.0 + 0.5

        # plot red only for pilots that never started
        if not running:
            running = ltf + 1

        eb.broken_barh([(new, running-new)], (y-cores/2.0+.1, cores-.2), edgecolor=color,
                facecolor=color, label='Pilot Queue')

        cum_cores += cores

    # CU Life Times
    for pilot, name, cores, state, errno, download, run, upload, end, site in cus:
        colors=['yellow', 'green', 'orange']
        hatch = None
        if run == 0:
            run = end
            upload = end
            #colors=['black', 'black', 'black']
            hatch='x'
        # TODO: what if execution or upload fails?
        # eb.broken_barh([(download, run-download),
        #                  (run, upload-run),
        #                  (upload, end-upload)], (pilots[pilot]-0.3, .6),
        #                  facecolor=colors,
        #                  hatch=hatch, label='CU')
        eb.broken_barh([(download, run-download),
                         (run, upload-run),
                         (upload, end-upload)], (pilots[pilot]-.3, .6),
                         facecolor=colors, edgecolors=colors,
                         hatch=hatch, label='CU', color='None')

        #plt.fill(x,np.sin(x),color='blue',alpha=0.5)
        #plt.fill(x,np.sin(x),color='None',alpha=0.5,edgecolor='blue',hatch='/')

    # TaskQueue length
    q_t = []
    q_l = []

    for t,l in tq:
        q_t.append(t)
        q_l.append(l)

    tq = plt.twinx()
    #ax2.step(q_t, q_l, '--', color='black')
    tq.plot(q_t, q_l, 'r--', color='blue', drawstyle='steps-post', linewidth=2.0, label='CU Queue Length')
    
    tq.ticklabel_format(style='plain')
    tq.set_ylabel('Waiting ComputeUnits')

#    ya = tq.get_yaxis()
#    ya.set_major_locator(MaxNLocator(integer=True))

    #plt.ylim(0,10)
    #plt.xlim(1353410004-100, ltf+100)

    # Get handles and labels for both eb and tq
    handles, labels = eb.get_legend_handles_labels()
    hl, lb = tq.get_legend_handles_labels()
    handles.extend(hl)
    labels.extend(lb)
    
    # custom proxy artists (for unsupported artists) 
    p = Rectangle((0, 0), 1, 1, fc='red')
    handles.append(p)
    labels.append('CP Queued')
    
    p = Rectangle((0, 0), 1, 1, fc='yellow')
    handles.append(p)
    labels.append('CU Staging-In')
     
    p = Rectangle((0, 0), 1, 1, fc='green')
    handles.append(p)
    labels.append('CU Execution') 
     
    p = Rectangle((0, 0), 1, 1, fc='orange')
    handles.append(p)
    labels.append('CU Staging-Out')

    p = Rectangle((0, 0), 1, 1, fc='white', hatch='xxx')
    #p = Rectangle((0, 0), 1, 1, fc='black')
    handles.append(p)
    labels.append("Failed") 
    
    # draw the legend 
    eb.legend(handles, labels, loc=2)

    plt.title('ComputePilot Lifetimes with ComputeUnit Queue Length')

    plt.show()

    #fig2 = matplotlib.pyplot.figure(figsize=(8.0, 5.0)) # in inches!
    #plt.savefig('fig.pdf', format='pdf', bbox_inches=(10,5), dpi=600)



def last_cu_done(cus):

    # keep track of the finishing time of the last compute unit
    last = 0

    for cu in cus:
        done = cu[7]
        #done = cu[4]
        last = max(last, done)

    return last


if __name__ == '__main__':

    # Compute Pilots
    #  tuples of (0:cores, 1:new, 2:running, 3:end )
    my_pilot_lifetimes = [
        (1, 1, 2, None),
        (2, 2, 3, 8),
        (3, 3, 4, 8),
        (4, 4, 5, 10)
    ]

    # Compute Units
    # tuplics of (0:pilot, 1:name, 2:cores, 3:state, 4:errno, 5:download, 6:run, 7:upload, 8:end, 9:site)
    my_cus = [
        (0, "cu0", 1, "Done", 0, 2, 4,  6, 7, "stampede"),
        (1, "cu1", 1, "Done", 0, 4, 5,  7, 8, "stampede"),
        (2, "cu2", 2, "Done", 0, 5, 6,  8, 9, "stampede"),
        (0, "cu3", 4, "Done", 0, 12,13,16,18, "stampede")
    ]

    # TaskQueue
    # Tuples of (0:Time, 1:Length)
    my_tq = [(0,0), (1,4), (2,3), (3,2), (10,1), (15,0) ]

    #my_pilot_lifetimes, my_cus, my_tq, my_start, my_stop = \
    #        parse_file('test11.log')

    my_ltf = last_cu_done(my_cus)

    print my_pilot_lifetimes
    print my_cus
    print my_tq

    plot_pilotlifetime(my_pilot_lifetimes, my_cus, my_tq, my_ltf)
