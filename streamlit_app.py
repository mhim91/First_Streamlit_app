import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

##simulation functions
# 
# 

# Initialize the variable in session_state if it doesn't exist yet
if 'time' not in st.session_state:
    st.session_state.time = 0
if 'x' not in st.session_state:
    st.session_state.x = 1
if 'y' not in st.session_state:
    st.session_state.y = 0
if 'vx' not in st.session_state:
    st.session_state.vx = 0
if 'vy' not in st.session_state:
    st.session_state.vy = 1
if 'x_list' not in st.session_state:
    st.session_state.x_list = [1]
if 'y_list' not in st.session_state:
    st.session_state.y_list = [0]
if 'G' not in st.session_state:
    st.session_state.G = 1
if 'M' not in st.session_state:
    st.session_state.M = 1
if 'dt' not in st.session_state:
    st.session_state.dt = 0.0001
if 'dx' not in st.session_state:
    st.session_state.dx = 0.002
if 'jupiter_phi' not in st.session_state:
    st.session_state.jupiter_phi = 0
if 'jupiter_distance' not in st.session_state:
    st.session_state.jupiter_distance = 4
if 'jupiter_mass' not in st.session_state:
    st.session_state.jupiter_mass = 0.01

#functions

def Period(a):
    return np.sqrt(4 * np.pi**2 * a**3 / (st.session_state.G*st.session_state.M))

def Acc(x,y, x0 = 0, y0 = 0, M = st.session_state.M):
    d = np.sqrt((x - x0)**2 + (y - y0)**2)
    k = st.session_state.G*M/(d**3)
    return np.array([-(x - x0)*k, -(y - y0)*k])

def jupiter_coordinates(t):
    phi = st.session_state.jupiter_phi + 2*np.pi*t/Period(st.session_state.jupiter_distance)
    x = st.session_state.jupiter_distance * np.cos(phi)
    y = st.session_state.jupiter_distance * np.sin(phi)
    return x,y


def step(x,y,vx, vy, dt):
    xm, ym = jupiter_coordinates(st.session_state.time)

    acc = Acc(x,y) + Acc(x,y, xm, ym, st.session_state.jupiter_mass)

    ax = acc[0]
    ay = acc[1]

    vx_0 = vx
    vy_0 = vy

    vx = vx + ax*dt
    vy = vy + ay*dt

    x = x + (vx +  vx_0)*dt / 2
    y = y + (vy +  vy_0)*dt / 2

    return x,y,vx,vy

def vis_viva_vel(r,a):
    return np.sqrt(st.session_state.G*st.session_state.M*(2/r - 1/a))

def tangential_boost(vx,vy, Dv):
    v = np.sqrt(vx**2 + vy**2)
    return (vx/v)*(v + Dv), (vy/v)*(v + Dv)

def velocity(vx,vy):
    return np.sqrt(vx**2 + vy**2)



def update_simulation():
    newtime = st.session_state.time + wait_time_input
    while st.session_state.time < newtime:
        timestep = st.session_state.dx / velocity(st.session_state.vx, st.session_state.vy);
        st.session_state.x, st.session_state.y, st.session_state.vx, st.session_state.vy = step(st.session_state.x, st.session_state.y, st.session_state.vx, st.session_state.vy, timestep)
        st.session_state.x_list.append(st.session_state.x)
        st.session_state.y_list.append(st.session_state.y)
        st.session_state.time += timestep
    

def return_figure():
    fig, ax = plt.subplots()
    ax.plot(st.session_state.x_list, st.session_state.y_list)
    ax.plot(st.session_state.x, st.session_state.y, marker = 'o', label = "Satellit", color = 'black')
    ax.plot(0, 0, marker = 'o', label = "Solen", color = 'orange')

    xm, ym = jupiter_coordinates(st.session_state.time)
    ax.plot(xm, ym, marker = 'o', label = "Planet", color = 'red')

    ax.set_aspect('equal', adjustable='box')
    plt.legend(loc = 'upper right')
    ax.set_box_aspect(1)
    plt.grid(True)
    ax.set_xlim([-8, 8])
    ax.set_ylim([-8, 8])
    return fig



#gui code


st.title("Hohmannbanor")


col1, col2 = st.columns(2)

with col1:
    st.pyplot(return_figure())
    # Example matplotlib plot (renders in Streamlit)


    st.write("Aktuellt tillstånd: x = ", st.session_state.x,
            "y = ", st.session_state.y,
            "vx = ", st.session_state.vx,
            "vy = ", st.session_state.vy,
            "v = ", velocity(st.session_state.vx, st.session_state.vy))

with col2:

    wait_time_input = st.number_input('Väntetid', placeholder = 1)

    if st.button("Vänta"):
        update_simulation()
        st.rerun()

    boost_input = st.number_input('Boost ammount:', placeholder = 0)

    if st.button("Boosta"):
        st.session_state.vx, st.session_state.vy = tangential_boost(st.session_state.vx, st.session_state.vy, boost_input)  
        st.pyplot(return_figure())
        st.rerun()

    if st.button("Reset", type="primary"):
        # Clear all items in session state
        st.session_state.clear()
            # Force a rerun to show the clean state
        st.rerun()
