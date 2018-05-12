import tkinter as tk
from em340.em340 import Em340
from em340.measurement import Measurement
from helper.combinatoric_calculator import CombinatoricCalculator
import argparse

def write_measurment(p,s,q,i,devLabel):
    port = 'COM17' # serial port
    parser = argparse.ArgumentParser()
    parser.add_argument("--p", help="serial port where your modbus device is plugged in, e.g. COM4")
    args = parser.parse_args()

    if args.p:
        port = args.p
    em340 = Em340(port)
    measurement = em340.read_phase1()
    p.config(text="Leistung P:= {0} W".format(measurement.p))
    s.config(text="Scheinleistung S:= {0} VA".format(measurement.s))
    q.config(text="Blindleistung Q:= {0} VAR".format(measurement.q))
    i.config(text="Stromverbrauch I: {0} A".format(measurement.i))

    calculator = CombinatoricCalculator()
    result =calculator.calculate(measurement.p,measurement.s,measurement.q,measurement.i)
    devLabel.config(text=result)


root = tk.Tk()
root.title("Smart Meter")
frame = tk.Frame(root, width=250, height = 100)
frame.pack_propagate(0)
frame.grid(padx=50, pady=50)
frame.pack(fill=None, expand=True)


labelTotal = tk.Label(root,text="Verbrauch Total:",font="Helvetica 10 bold")
labelTotal.pack()

labelP = tk.Label(root,text="Leistung P:")
labelP.pack()

labelQ = tk.Label(root,text="Blindleistung Q:")
labelQ.pack()

labelS = tk.Label(root,text="Scheinleistung S:")
labelS.pack()

labelI = tk.Label(root,text="Stromverbrauch I:")
labelI.pack()

labelTitle = tk.Label(root,text="Aktive Geräte:",font="Helvetica 10 bold")
labelTitle.pack()

label = tk.Label(root,text=".....")
label.pack()

button = tk.Button(frame,
                   text="Messen",
                   command=lambda:write_measurment(labelP,labelS,labelQ,labelI,label))
button.grid(padx=50, pady=10)



root.mainloop()