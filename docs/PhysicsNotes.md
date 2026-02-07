# Physics Notes
- This file will focus on relevant physics and fundamental equations for the production of Eragon, aka first-principles thinking

### International System of Units (SI)
- Units of measurements
- Base constants that can have an unlimited number of derivations
    - Base Units
        - **second** for time (s)
        - **meter** for length/distance (m)
        - **kilogram** for mass (kg)
        - **ampere** for electric current (A)
        - **kelvin** for thermodynamic temperature (K)
        - **mole** for amount of substance (mol)
        - **candela** for luminous intensity (cd)
    
            !['See SI units image in 05_Images'](..\05_Images\SI_units.png)

- Set of mutually independent dimensions, dimensional analysis

### Elementary Charge Carriers
- Particles or Quasi-particles that carry an electric charge
    - Electrons/Ions/Holes
- Elementary Charges = $e$

### Electrons
- fundamental subatomic particle that carries a negative elementary electric charge 
    - electric charge = $-1.602*10^{-19}$ coulombs
    - mass = $9.109 * 10^{-31}$ kg 
        - 'lightest known stable particle'
- exhibit both particle/wave-like behaviors


### Atoms
- Smallest unit of *matter*, that retains properties of elements
- 3 subatomic particles
    - Neutrons( )/Protons(+)/Electrons(-)
        - Protons/Neutrons = Nucleus
        - Electrons = Electron Shells
    
### Element
- A **pure** substance made up of **1 type of atom**. 
- Defined by the number of protons in the nucleus.
- Each element is unique and cannot be broken down into simpler substances?
- See the **Periodic Table** where it defines each element.
    - i.e. oxygen has 8 protons, hence it's atomic number is 8
- Chemical properties stay the same based on **electron configuration**

#### Ion 
- An element with changes in the number of **Electrons**
- Adding/Removing electrons causes a distortion/change in state of an atom
    - Cation **Removing an electron**
        - Atom is positively charged
    - Anion **Adding an electron**
        - Atom is negatively charged

- ##### Valence Shell Pair Repulsion Theory (VSEPR) 
    - Atoms tend towards the most stable state
    - A useful algorithm for predicting the geometry of atoms
        - It breaks down in unique and complicated arrangements

## Electricity
- Arises from the presence, motion and interactions of electric charges. Attraction/Repulsion.
- A low-entropy form of energy
- non-equilibrium thermodynamics
- Governed by Ohm's Law
    - $V = I*R$
    - #### Voltage
        - $V$ = Voltage (Potential Difference/Tension/Pressure in charge)
            - The build up of electric charge
                - Electron Elementary charge ($e$) = $-1.602*10^{-19}$
            - A physical scalar quantity
            - The source, loss, dissipation, or storage of energy
            - Higher Voltage -> Lower Voltage
    - #### Current
        - $I$ = Current/Amperage (How many electrons/Coulombs passing at a point per second)
            - Amperage/Amp(s) = base SI unit (see above)
            - "Net rate of flow of electric charge through a surface"
                - Electron/Proton are equal in magnitude? but opposite signs
                    - hence, electrically neutral atoms when equivalent electrons/protons
            - $1A = 1C/s = \frac{1}{1.602*10^{-19}}$ e/s = $\frac{10^{19}*e}{1.602s}$
            - 1 Amp = 1 Coulomb per second
            - Quarks etc. (Out of scope for Eragon)
    - #### Resistance/Conductance
        - $R$ = Resistance (Difficulty in electrons to pass/friction)
            - A measure of the opposition to the flow of electrons
                - Can be measured on the **difficulty** or **ease** of electron passage (based on frame of reference)
            - Electrical Resistance (Ohms $\Omega$) or Conductance (Siemans $S$)
            - Resistance is dependant on material
                - All objects are conductors
                    - Ease of valence electron or ion movement determines if it is a good Conductor/Insulator
        - ##### Temperature
            - Influences motion of atoms/electrons, thus affects resistance
                - Resistance $R = R_0(1 + \alpha(T - T_0))$
                    - $R_0$ = Base Resistance at reference $T_0$
                    - $\alpha$ = Temp Coefficient, material specific
                        - how much resistance changes per degree of temp change for the specific material
                        - Copper $\alpha$ = 0.00393/$\degree C$
                - Temp sensors take advantage of this! (see Thermisistors)
                - Limitations of equation
                    - Extreme Temps need more precise measurements, as the linearity of the resistance change is assumed!
                    - Superconductors are different
                    - Impurities/Strain/Magnetic fields can alter $\alpha$


### Electrical Wires

- #### Wire Resistance
    - Resistance $R = \rho \frac{L}{A}$
        - $\rho$ = Resistivity of material (look at material properties)
            - i.e. Silver $\rho = 1.59 * 10^-8 \Omega * m$
        - $L$ = Length of wire (Electron Collisions)  
        - $A$ = Cross-sectional area of the wire (Freedom of movement)

- #### Current Density
    - Measure of how many amps is passing in a particular area of a wire
    - Current density can explain heating/efficiency/safety issues
    - high density = overheating, low density = smooth flow
        - Current Density $J = \frac{I}{A}$
            - Current Density $J$ in Amperes/$m^2$
            - $I$ = Total Current flowing in wire (Amps)
            - $A$ = Cross-sectional area of the wire
    - Typically $\vec{J}$ But were assuming a straight wire! Only need the scalar value 

## Semiconductor
- Material with electrical conductivity between that of a conductor and an insulator
    - Conductivity is modified by adding impurites to it's structure
        - aka **Doping**
    - ##### **Dies (i.e. silicon die)** 
        - a small thin slice/block (i.e. silicon) on which an entire integrated circuit is fabricated
        - can hold things like the microprocessor/memory chip   

#### Isotopes
- An element with changes in the number of **Neutrons**
    - Adding neutrons destabilizes the nucleus, leading to radioactive decay
        - i.e. beta-minus decay might cause a neutron to become a proton, effectively changing the element over time. 
    - Look into neutron capture? (out of scope for Eragon)
    
### Density
- quantifies mass of a substance per unit volume, how compact/concentrated a material is. 
- $p = \frac{m}{V}$
- SI unit = $\frac{kg}{m^3}$
    - i.e. Aluminum is 2.699 grams/cm^3

### Gravity
- The force that attracts all objects with mass towards each other.
- A fundamental force that will *always* be acting on Eragon. 
- *Everything* has a gravitational pull (affects spacetime), although most are assumed miniscule to irrelevant in calculations. 
    - Newton's Law of Universal Gravitation
        - The gravitational force between two masses is based on mass and distance to each other. 
        - $F$ = $G\frac{m_1 m_2}{r^2}$
            - $F$ = Magnitude of the gravitational force between two objects
            - $G$ = The gravitational constant ~6.674*10^-11
            - $r$ = The distance between the two centers of mass (in meters)
        - The above applies to *specifically point-masses/spherical objects* at their center
        - This law applies *universally* regardless of location in space
#### Earth **9.80665 m/s/s**
- Assuming no air resistance
- Net acceleration imparted to objects due to combined effects of Earth's gravitational pull and the centrifugal force from it's rotation. 
- Earth Gravitational Effects
    - The **centrifugal effect** of earth's rotation makes the equator reduce gravity by ~0.3% 
    - Earth **bulges at the equator** = further from the center = less gravitational pull
    - Geology, **local rock densities** and topography (mountains/underground deposits) cause local gravity anomalies 

#### Deep Space **~0 m/s/s**
- Gravity is miniscule in deep space, distance (m) reduces gravity's effect squared
    - $F$ = $G\frac{m_1 m_2}{r^2}$
    - no nearby mass = negligible acceleration

#### Moon **~1.62 m/s/s**
- Mass = 



### Scientists
- Michael Faraday (Ions)
- William Whewell (Ions)
- Lord Kelvin (Temperature)
- Andre-Marie Ampere (Electricity)
- J.J. Thomson (Electrons)
- Gustav Kirchoff (Voltage)

### Measurement Tools
- Voltmeter
    - measure the voltage between two points in a system.
- NTC Thermisistors (Negative Temperature Coefficient)
    - measures the resistance drop as temp rises

