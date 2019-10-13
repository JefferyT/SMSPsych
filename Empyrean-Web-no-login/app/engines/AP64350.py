# Performs calculations given the form for AP64500 and AP64350 parts
# Returns output to be displayed and creates graphs for power loss, efficiency,
# and compensation

import os
import math
import cmath
from decimal import Decimal as D
from matplotlib import pyplot as plt
import matplotlib as mpl

def sim(form_data):
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    
    #Form data
    part_number = form_data["part_number"]
    switching_frequency = form_data["switching_frequency"]
    output_voltage = form_data["output_voltage"]
    output_current = form_data["output_current"]
    input_voltage = form_data["input_voltage"]
    ripple_ratio = form_data["ripple_ratio"]
    output_inductor = form_data["output_inductor"]
    dcr = form_data["dcr"]
    num_capacitors = form_data["num_capacitors"]
    capacitance_each = form_data["capacitance_each"]
    esr_each = form_data["esr_each"]
    v_on = form_data["v_on"]
    v_off = form_data["v_off"]
    thermal_resistance = form_data["thermal_resistance"]
    ambient_temperature = form_data["ambient_temperature"]
    min_current = form_data["min_current"]
    max_current = form_data["max_current"]
    R5_s = form_data["R5_selected"]
    C5_s = form_data["C5_selected"]
    C6_s = form_data["C6_selected"]
    user_selects_R2 = form_data["user_selects_R2"]
    user_selects_C4 = form_data["user_selects_C4"]

    #Power Loss Calculation
    output = {}
    rds_on_u = D(0.0)
    rds_on_l = D(0.0)
    R5 = D(0.0)
    R6 = D(0.0)
    vgs_u = D(0.0)
    vgs_l = D(0.0)
    recommended_inductor  = D(0.0)
    if part_number == 'AP64350':
        rds_on_u = D(80.0)
        rds_on_l = D(50.0)
    else:
        rds_on_u = D(45.0)
        rds_on_l = D(20.0)


    rds_on_uc = (rds_on_u * (1 + D(0.005) * (ambient_temperature - 25)) * (1 + rds_on_u * D(0.001) *
                (output_current)**2 * output_voltage / input_voltage))
    rds_on_lc = (rds_on_l * (1 + D(0.005) * (ambient_temperature - 25)) *(1 + rds_on_l *
                D(0.001) * (output_current)**2 * (1 - (output_voltage / input_voltage))))

    current_ripple = D((input_voltage - output_voltage) * 
                     (output_voltage/(input_voltage * output_inductor * D(10**(-6)) 
                     * switching_frequency * D(10**3))))
    duty_cycle = ((output_voltage + (output_current * (dcr + rds_on_lc) / 1000)) / 
                 (input_voltage + (output_current * D((rds_on_lc - rds_on_uc) / 1000))))
    on_time = duty_cycle * 10**9 / (switching_frequency * 1000)
    effective_output_resistance = output_voltage / output_current
    upper_rms = (output_current * D(math.sqrt(duty_cycle))
                * D(math.sqrt(1 + D(1/3) * D((current_ripple / 2 /  output_current)**2))))
    lower_rms = (output_current * D(math.sqrt(1 - duty_cycle)) * 
               D(math.sqrt(1 + D(1/3) * D((current_ripple / 2 / output_current)**2))))
    output_voltage_ripple = (current_ripple * esr_each / num_capacitors + current_ripple / 
                            (8 * switching_frequency * num_capacitors * capacitance_each * D(10**(-6))))

    if v_on == 3.7:
        R5 = 'OPEN'
        R6 = 'OPEN'
    else:
        R5 = (D(0.935) * v_on - v_off) / D(0.0041)
        R6 = D(1.1) * R5 / (v_off - D(1.1) + (D(0.0055) * R5))
    
    RT = 10**5 / switching_frequency

    #UPPER MOSFET
    Vd = D(1.2)
    Qrr = D(0.3)
    Qg = D(0.2)
    Cgs = 30 / rds_on_uc
    Coss_u = 20 / rds_on_uc
    Tr = 15
    Tf = 12
    n = 1
    Pcon_u = (upper_rms)**2 * rds_on_uc / n / 1000
    Psw_on = (input_voltage * (output_current - D(0.5) * current_ripple) * Tr * D(10**(-9)) *
             switching_frequency * D(10**3) / 2)
    Psw_off = (input_voltage * (output_current + D(0.5) * current_ripple) * Tf
              * D(10**(-9)) * switching_frequency * D(10**3) / 2)
    Pdiode = input_voltage * switching_frequency * D(10**3) * Qrr * n * D(10**(-9))
    Pcap = D(0.5) * Coss_u * D(10**(-9)) * (input_voltage)**2 * switching_frequency * D(10**3) * n

    Pupper = Pcon_u + Psw_on + Psw_off + Pdiode + Pcap

    #LOWER MOSFET
    Cgs = 30 / rds_on_lc
    Coss_l = 20 / rds_on_lc
    Td_on = D(20.2)
    Td_off = D(28.2)
    Pcon_l = (lower_rms)**2 * rds_on_lc / 1000 / n
    Pdiode = (Vd * switching_frequency * D(10**(-6)) * ((output_current + D(0.5) * current_ripple) * Td_on
             + ((output_current - D(0.5) * current_ripple) * Td_off)))
    Pdiode_QRR = D(0.5) * Qrr * input_voltage * switching_frequency * D(10**(-6)) * n
    Pcap = Coss_l * D(10**(-9)) * n * (input_voltage)**2 * switching_frequency * 1000 / 2
    Plower = Pcon_l + Pdiode + Pdiode_QRR + Pcap

    #DRIVER POWER LOSS
    if input_voltage < 5.7:
        vgs_u = input_voltage
        vgs_l = input_voltage
    else:
        vgs_u = 5
        vgs_l = 5
    Iq = 6
    Pdr_up = switching_frequency * vgs_u * Qg * n * D(10**(-6))
    Pdr_low = switching_frequency * vgs_l * Qg * n * D(10**(-6))
    LDO = (input_voltage - vgs_l) * Iq / 1000
    Pdriver = Pdr_up + Pdr_low + LDO + Iq * vgs_l * D(0.001)

    #OUTPUT INDUCTOR LOSS
    Pcore = (D(0.7 * 10**(-9)) * (switching_frequency)**(D(1.35)) * (D(57.8 * 0.5) * current_ripple)**(D(2.263)))
    Pcon_oi = dcr / 1000 * (output_current * D(math.sqrt(1 + D(1/3) * (current_ripple / output_current)**2)))**2
    Pind = Pcore + Pcon_oi

    #OUTPUT CAPACITOR LOSS
    Pesr = (D(0.5) * current_ripple / D(math.sqrt(3))**2 * (esr_each / num_capacitors / 1000))

    total_loss = Pdriver + Plower + Pupper + Pind
    efficiency = ((output_voltage * output_current) / (output_voltage * output_current + total_loss) * 100)

    power_dissipation = Pupper + Plower + Pdr_up + Pdr_low
    junction_temperature = ambient_temperature + thermal_resistance * power_dissipation
    
    if part_number == 'AP64350':
        recommended_inductor = max(
        (((input_voltage - output_voltage) * duty_cycle) / 
        (switching_frequency * 10**3 * D(3.5) * ripple_ratio / 100) * 10**6),
        (output_voltage * D(0.089 * 10**6)) / D((0.8 * 1.87 * 5 * 10**5))) 
    else:
        recommended_inductor = max(
        (((input_voltage - output_voltage) * duty_cycle) /
        (switching_frequency * 10**3 * 5 * ripple_ratio / 100) * 10**6),
        (output_voltage * D(0.089 * 10**6)) / D((0.8 * 1.87 * 5 * 10**5)))

    output["recommended_inductor"] = round(recommended_inductor, 1)
    output["rds_on_u"] = rds_on_u
    output["rds_on_l"] = rds_on_l
    output["total_loss"] = round(total_loss, 3)
    output["efficiency"] = round(efficiency, 3)
    output["on_time"] = round(on_time)
    output["duty_cycle"] = round(duty_cycle, 2)
    output["effective_output_resistance"] = round(effective_output_resistance, 1)
    output["upper_rms"] = round(upper_rms, 2)
    output["lower_rms"] = round(lower_rms, 2)
    #output["lower_rms"] = lower_rms
    output["current_ripple"] = round(current_ripple, 2)
    output["output_voltage_ripple"] = round(output_voltage_ripple)
    output["R5"] = round(R5)
    output["R6"] = round(R6)
    output["RT"] = round(RT)
    output["junction_temperature"] = round(junction_temperature, 1)
    output["power_dissipation"] = round(power_dissipation, 3)
    
    # Power Loss graph
    fig = plt.figure()
    plt.style.use('seaborn-whitegrid')
    fig.set_size_inches(7.25, 5)
    ax = fig.add_subplot(1, 1, 1)
    x_axis = ["", "Upper MOSFET", "Lower MOSFET", "Driver", "Output Inductor", "Output Cap. ESR"]
    y_axis_top = [Pupper, Plower, (Pdr_up + Pdr_low), Pind, 0]
    y_axis_bot = [Pcon_u, Pcon_l, 0, Pcon_oi, Pesr]
    x_axis_plot = [1, 2, 3, 4, 5]
    width = D(0.35)
    ax.plot = plt.bar(x_axis_plot, y_axis_top, width, color='r', label='Switching Losses')
    ax.plot = plt.bar(x_axis_plot, y_axis_bot, width, color='#005595', label='Conducting Losses')
    ax.set_title('Power Loss Distribution Chart')
    ax.set_xticklabels(x_axis)
    ax.legend()

    fig.savefig(os.path.join(fileDir, 'app/static/images/power_loss.png'))
    plt.close(fig)

    #Efficiency Loss Calculation
    dcm_ccm_boundary = current_ripple / 2
    output["dcm_ccm_boundary"] = round(dcm_ccm_boundary,  2)
    current_dif = max_current - min_current

    output_current_l = [min_current, min_current + current_dif * D(0.001)]
    i = D(0.002)
    while i <= 0.0101:
        #print(i)
        output_current_l.append(min_current+current_dif * i)
        i += D(0.002)
    i = D(0.02)
    while i <= 0.1:
        #print(i)
        output_current_l.append(min_current+current_dif * i)
        i += D(0.02)
    i = D(0.15)
    while i <= 1.01:
        #print(i)
        output_current_l.append(min_current+current_dif * i)
        i += D(0.05)
    output_current_l.pop(15)
   
    time_shift, frequency, rip_1, rip_2, up_rms, os_rms = ([] for i in range(6))
    losses_um, losses_lm, driver_loss, inductor_loss, capacitor_loss = ([] for i in range(5))
    total_loss_list, efficiency_list = ([] for i in range(2))

    for i in range(0, len(output_current_l)):
        if output_current_l[i] > dcm_ccm_boundary:
            time_shift.append(0)
        else:
            time_shift.append(
                (2 / ((input_voltage - output_voltage) * output_voltage/
                (2 * input_voltage * output_inductor * D(0.000001) * 
                (dcm_ccm_boundary-output_current_l[i])))))
        
        frequency.append(1 / (1000 / (switching_frequency * 1000)+ time_shift[i] * 1000))
        rip_1.append(
                (output_voltage / input_voltage * (1 + (rds_on_lc + dcr) / 1000 * output_current_l[i]
                / output_voltage) / (1 - output_current_l[i] * (rds_on_uc-rds_on_lc) / 1000 / input_voltage)))
        rip_2.append(
                ((input_voltage - output_voltage) / output_inductor / D(10**(-6)) * 
                rip_1[i] / switching_frequency / D(10**(3))))
        up_rms.append(
                (output_current_l[i] * D(math.sqrt(rip_1[i])) * D(math.sqrt(1 + D(1/3) * 
                (rip_2[i] / 2 / output_current_l[i])**2))))
        os_rms.append(
                (output_current_l[i] * D(math.sqrt(1 - rip_1[i])) * D(math.sqrt(1 + D(1/3) *
                (rip_2[i] / 2 / output_current_l[i])**2))))
        losses_um.append(
                (up_rms[i])**2 * rds_on_uc / n / 1000 +
                input_voltage * (output_current_l[i] - D(0.5) * rip_2[i])
                * Tr * D(10**(-9)) * frequency[i] * 10**3 / 2 +
                input_voltage * (output_current_l[i] + D(0.5) * rip_2[i])
                * Tf * D(10**(-9)) * switching_frequency * 10**3 / 2 + 
                input_voltage * frequency[i] * 10**3 * Qrr * D(10**(-9)) * n + 
                D(0.5) * Coss_u * D(10**(-9)) * (input_voltage)**2 * frequency[i] * 10**3 * n)
        losses_lm.append(
                (os_rms[i]**2 * rds_on_lc / 1000 / n +
                Vd * frequency[i] * D(10**(-6)) * ((output_current_l[i] + D(0.5) * rip_2[i])* Td_on
                + (output_current_l[i] - D(0.5) * rip_2[i]) * Td_off)
                + D(0.5) * Qrr * input_voltage * frequency[i] * D(10**(-6)) * n
                + Coss_l * D(10**(-9)) * n * input_voltage**2 * frequency[i] * 1000 / 2))
        driver_loss.append(
                (frequency[i] * vgs_u * Qg * D(10**(-6)) * n 
                + frequency[i] * vgs_l * Qg * D(10**(-6)) * n + vgs_l * Iq * D(0.001)))
        inductor_loss.append(
                (D(0.7) * D(10**(-9)) * frequency[i]**(D(1.35)) * 
                (D(57.8) * D(0.5) * rip_2[i])**(D(2.263)) + dcr/1000 * (output_current_l[i] * 
                D(math.sqrt(1 + D(1/3) * (rip_2[i] / output_current_l[i])**2)))**2))
        capacitor_loss.append(
                ((D(0.5) * rip_2[i] / D(math.sqrt(3)))**2 * esr_each / num_capacitors / 1000))
        total_loss_list.append(D(losses_um[i] + losses_lm[i] + driver_loss[i]
                + inductor_loss[i] + capacitor_loss[i]))
        efficiency_list.append(D(output_voltage * output_current_l[i] / 
                (output_voltage * output_current_l[i] + total_loss_list[i]) * 100))


    # Efficiency graph
    fig = plt.figure()
    fig.set_size_inches(7.25, 5)
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(output_current_l, efficiency_list, color="black", linewidth=3)
    ax.set_title('Efficiency vs. Load')

    fig.savefig(os.path.join(fileDir, 'app/static/images/Efficiency.png'))
    plt.close(fig)

    
    # Compensation Calculations
    omega_o = D(math.sqrt(1/(output_inductor * D(10**(-6)) * num_capacitors * 
                       D(10**(-6)) * capacitance_each *
                       (effective_output_resistance + esr_each * D(0.001) / num_capacitors) /
                       (effective_output_resistance + dcr * D(0.001)))))
    fesr = 1 / (2 * D(math.pi) * capacitance_each * D(10**(-6)) * esr_each * D(0.001))
    fz = 1 / (2 * D(math.pi) * capacitance_each * D(10**(-6)) * num_capacitors * (
        esr_each * D(0.001) / num_capacitors + output_voltage / output_current))
    q = 1 / (omega_o * (capacitance_each * D(10**(-6)) * esr_each * D(0.001) * output_voltage / 
        (output_current * (output_voltage / output_current + dcr * D(0.001))) + 
        (output_voltage / output_current + esr_each * D(0.001)) * capacitance_each * D(10**(-6)) *
        num_capacitors * dcr * D(0.001) / (output_voltage / output_current + dcr * D(0.001))
        + output_inductor * D(10**(-6)) / (output_voltage / output_current + dcr * D(0.001))))
    fs = switching_frequency * 1000
    output["omega_o"] = format(omega_o, ".2E")
    output["fesr"] = round(fesr)
    output["fz"] = round(fz)
    output["q"] = round(q, 3) 
    output["fs"] = format(fs, ".2E")
    trans_resistance = D(0.089)
    slope_compensation = D(1.87)
    current_sense = trans_resistance * (input_voltage - output_voltage) / (output_inductor * D(10**(-6)))
    total_control_slope = 1 + slope_compensation * fs / current_sense
    error_amp = 10**(7)
    feedback_voltage = D(0.8)
    transconductance = D(0.00015)
    desired_fc = D(0.1) * fs
    R5_c = (2 * D(math.pi) * output_voltage * capacitance_each * num_capacitors * D(10**(-6))
             * desired_fc * trans_resistance / (transconductance * feedback_voltage))
    C5_c = 1 / (2 * D(math.pi) * R5_c * fz)
    C6_c = 1 / (2 * D(math.pi) * R5_c * fs * D(0.5))
    Fz1_c = 1 / (2 * D(math.pi) * R5_c * C5_c)
    Fp2_c = 1 / (2 * D(math.pi) * R5_c * C6_c)
    Fz1_s = 1 / (2 * D(math.pi) * R5_s * C5_s)
    Fp2_s = 1 / (2 * D(math.pi) * R5_s * C6_s)
    output["current_sense"] = format(current_sense, ".2E")
    output["total_control_slope"] = format(total_control_slope, ".2E")
    output["R5_c"] = format(R5_c, ".2E")
    output["C5_c"] = format(C5_c, ".3E")
    output["C6_c"] = format(C6_c,".3E")
    output["Fz1_c"] = round(Fz1_c)
    output["Fp2_c"] = format(Fp2_c, ".3E")
    output["Fz1_s"] = round(Fz1_s)
    output["Fp2_s"] = format(Fp2_s, ".3E")
    user_selects_R1 = user_selects_R2 * (output_voltage / feedback_voltage - 1)
    output["user_selects_R1"] = round(user_selects_R1, 1)
  
    wn = D(math.pi) * fs
    Qn = D(-2 / math.pi)
    Fm = 1 / (total_control_slope * current_sense * (1 / fs))
    ii = 0
    Fstart = 100
    Fstop = 1000000
    Fstep = 200
    Step = 0.02
    
        #Calculations for the Sampling Transfer function
    f_loop, s_loop, real_he, imag_he, complex_he, gain_he, phase_he = ([] for i in range(7))
    Gain_1 = input_voltage / (effective_output_resistance + dcr / 1000)
    u_complex1, l_complex1, l_complex2, l_complex3, l_complex4, fdi_s = ([] for i in range(6))
    Gain_2 = input_voltage/(1+((dcr * D(10**(-3)))/effective_output_resistance))
    u_complex2, ower_1, ower_2, fdv_s = ([] for i in range(4))
    ti_s, gain_clg, phase_clg, tv_s, gain_olvg, phase_olvg, t_s, gain_tlg, phase_tlg = ([] for i in range(9))
    z1_s, z2_s, t_gm_pole, t_gm_pole_cp1, t_pole_contrib, voltage_gain_denominator = ([] for i in range(6))
    k_s, top, bot_1, bot_2, bot_3, a_s = ([] for i in range(6))
    ks_as, compensator_mag, compensator_phase = ([] for i in range(3))
    tv_sc, vl_mag, vl_phase = ([] for i in range(3))
    ts_clc, gain_clc, phase_clc, o_gain, b_phase = ([] for i in range(5))

    ii=0
    while ii <=200:
        # Calctulations for the Sampling Transfer function
        f_loop.append(Fstart * 10**(Step * ii))
        s_loop.append(complex(0, 2 * math.pi * f_loop[ii]))
        real_he.append((s_loop[ii] * s_loop[ii])/complex((wn**2), 0) + 1)
        imag_he.append(s_loop[ii] / complex(wn * Qn, 0))
        complex_he.append(real_he[ii] + imag_he[ii])
        gain_he.append(20 * D(math.log(abs(complex_he[ii]), 10)))
        phase_he.append(cmath.phase(complex_he[ii]) * (180 / math.pi))

        # Open Loop to Inductor Current Transfer function
        u_complex1.append((1 + s_loop[ii] * complex(num_capacitors * (capacitance_each
        * D(10**(-6)) * (effective_output_resistance + (esr_each / (num_capacitors * 1000)))), 0)))
        l_complex1.append(s_loop[ii] * s_loop[ii] / complex((omega_o**(2))) + 1)
        l_complex2.append(s_loop[ii] / complex(q * omega_o, 0))
        l_complex3.append(l_complex1[ii] + l_complex2[ii])
        l_complex4.append(u_complex1[ii] / l_complex3[ii])
        fdi_s.append(complex(Gain_1, 0) * l_complex4[ii])

        # Open Loop duty Cycle to Output Voltage Transfer Function
        u_complex2.append(1 + s_loop[ii] * complex(num_capacitors * (capacitance_each
        * D(10**(-6)) * (esr_each / (num_capacitors * 1000))), 0))
        ower_1.append(l_complex1[ii] + l_complex2[ii])
        ower_2.append(u_complex2[ii] / ower_1[ii])
        fdv_s.append(complex(Gain_2, 0) * ower_2[ii])

        #Current Loop Gain
        ti_s.append(complex_he[ii] * fdi_s[ii] * complex(Fm * trans_resistance, 0))
        gain_clg.append(20 * cmath.log(abs(ti_s[ii]), 10))
        arg = cmath.phase(ti_s[ii]) * 180 / math.pi
        if arg < 0:
            phase_clg.append(arg + 180)
        else:
            phase_clg.append(arg - 180)

        #Open Loop Voltage Gain
        tv_s.append(fdv_s[ii] * complex(Fm, 0))
        gain_olvg.append(20 * cmath.log(abs(tv_s[ii]), 10))
        arg = cmath.phase(tv_s[ii]) * 180 / math.pi
        if arg < 0:
            phase_olvg.append(arg + 180)
        else:
            phase_olvg.append(arg - 180)

        #Total Loop Gain
        t_s.append(tv_s[ii] / (1 + ti_s[ii]))
        gain_tlg.append(20 * cmath.log(abs(t_s[ii]), 10))
        arg = cmath.phase(t_s[ii]) * 180 / math.pi
        if arg < 0:
            phase_tlg.append(arg + 180)
        else:
            phase_tlg.append(arg - 180)
        
        #Voltage Divider Gain

        z1_s.append(complex(user_selects_R1, 0)
                    / (1 + s_loop[ii] * complex(user_selects_R1 * user_selects_C4, 0)))
        z2_s.append(complex(user_selects_R2, 0) 
                    / (1 + s_loop[ii] * complex(user_selects_R2 * D(10**(-18)), 0)))
        t_gm_pole.append((1 + s_loop[ii] * complex(D(4.5 * 10**(-7)), 0)) 
                    / (s_loop[ii] * complex(D(4.5 * 10**(-11)), 0)))
        t_gm_pole_cp1.append(t_gm_pole[ii] / (1 + s_loop[ii] * t_gm_pole[ii] * 10**(-10)))
        t_pole_contrib.append(10000 + t_gm_pole_cp1[ii])
        voltage_gain_denominator.append(t_pole_contrib[ii] * z2_s[ii] / (t_pole_contrib[ii] + z2_s[ii]))

        #Gain of Internal Compensation
        k_s.append(z2_s[ii] / (z1_s[ii] + z2_s[ii]))
        top.append(1 + s_loop[ii] * complex(C5_s * R5_s, 0))
        bot_1.append(s_loop[ii] * s_loop[ii] * complex(R5_s * C5_s * C6_s, 0) + 1 / error_amp)
        bot_2.append(s_loop[ii] * complex(C5_s + C6_s + (C5_s * R5_s / error_amp), 0))
        bot_3.append(bot_1[ii] + bot_2[ii])
        a_s.append(complex(transconductance, 0) * (top[ii] / bot_3[ii]))
    
        #Compensator
        ks_as.append(k_s[ii] * a_s[ii] / ((1 + s_loop[ii] / (1.5 * 10**6))*
                    (1 + s_loop[ii] / (3.5 * 10**(7)))))
        compensator_mag.append(20 * math.log(abs(ks_as[ii]), 10))
        arg = cmath.phase(ks_as[ii]) * 180 / math.pi
        if arg < 0:
            compensator_phase.append(arg + 180)
        else:
            compensator_phase.append(arg - 180)

        # Voltage loop with compensation
        tv_sc.append(ks_as[ii] * complex(Fm, 0) * fdv_s[ii])
        vl_mag.append(20 * math.log(abs(tv_sc[ii]), 10))
        arg = cmath.phase(tv_sc[ii]) * 180 / math.pi
        if arg < 0:
            vl_phase.append(arg + 180)
        else:
            vl_phase.append(arg - 180)

        # Closed loop with compensation
        ts_clc.append(tv_sc[ii] / (1 + ti_s[ii]))
        gain_clc.append(20 * math.log(abs(ts_clc[ii]), 10))
        arg = cmath.phase(ts_clc[ii]) * 180 / math.pi
        if arg < 0:
            phase_clc.append(arg + 180)
        else:
            phase_clc.append(arg - 180)
        
        # To find the bandwith
        o_gain.append(1 - gain_clc[ii])
        b_phase.append(-1 * phase_clc[ii])

        ii+=1

    index = 0
    ii = 0
    smallest = abs(1 - o_gain[0])
    while ii < 200:
        ii += 1
        distance = abs(1 - o_gain[ii])
        if distance < smallest:
            smallest = distance
            index = ii
    bandwith = round(f_loop[index] / 1000, 2)
    phase_margin = round(phase_clc[index], 2)
    
    index = 0
    ii = 0
    smallest = abs(1 - b_phase[0])
    while ii < 200:
        ii += 1
        distance = abs(1 - b_phase[ii])
        if distance < smallest:
            smallest = distance
            index = ii
    gain_margin = round(gain_clc[index], 2)
    output["bandwith"] = bandwith
    output["phase_margin"] = phase_margin
    output["gain_margin"] = gain_margin


    # Compensation Graphs

    fig, axes = plt.subplots(3, 2)
    fig.set_size_inches(9, 10)
    axes[0,0].plot(f_loop, gain_clc, color="red", label="Bandwith of Closed Loop", linewidth=1.5)
    axes[0,0].set_title("Bandwith of Closed Loop")
    axes[0,0].set_xscale('log')
    axes[0,0].legend(loc='upper right')
    axes[0,0].grid(True)

    axes[0,1].plot(f_loop, phase_clc, color="blue", label="Phase Margin Closed Loop", linewidth=1.5)
    axes[0,1].set_title("Phase Margin of Closed Loop")
    axes[0,1].set_xscale('log')
    axes[0,1].legend(bbox_to_anchor=[1.3, 1], loc='upper right')

    axes[1,0].plot(f_loop, gain_tlg, color="red", label="T(s) Gain", linewidth=1.5)
    axes[1,0].plot(f_loop, gain_clg, color="blue", label="Ti(s) Gain", linewidth=1.5)
    axes[1,0].plot(f_loop, gain_olvg, color="#39ff14", label="Tv(s) Gain", linewidth=1.5)
    axes[1,0].set_xscale('log')
    axes[1,0].legend(bbox_to_anchor=[1.05, 1], loc='upper right')
    
    axes[1,1].plot(f_loop, gain_tlg, color="red", label="T(s) Phase", linewidth=1.5)
    axes[1,1].plot(f_loop, phase_clg, color="blue", label="Ti(s) Phase", linewidth=1.5)
    axes[1,1].plot(f_loop, phase_olvg, color="#39ff14", label="Tv(s) Phase", linewidth=1.5)
    axes[1,1].set_xscale('log')
    axes[1,1].legend(bbox_to_anchor=[1.15, 1], loc='upper right')

    axes[2,0].plot(f_loop, gain_tlg, color="red", label="T(s) w/o Comp", linewidth=1.5)
    axes[2,0].plot(f_loop, compensator_mag, color="#7FFFD4", label="Compensation", linewidth=1.5)
    axes[2,0].plot(f_loop, gain_clc, color="#B19CD9", label="T(s) with Comp", linewidth=1.5)
    axes[2,0].set_xscale('log')
    axes[2,0].legend()

    axes[2,1].plot(f_loop, phase_tlg, color="red", label="T(s) phase w/o comp", linewidth=1.5)
    axes[2,1].plot(f_loop, compensator_phase, color="#7FFFD4", label="Phase of Compensation", linewidth=1.5)
    axes[2,1].plot(f_loop, phase_clc, color="#B19CD9", label="T(s) with comp", linewidth=1.5)
    axes[2,1].set_xscale('log')
    axes[2,1].legend(bbox_to_anchor=[1.3, 1.15], loc='upper right')

    fig.savefig(os.path.join(fileDir,'app/static/images/Compensation.png'), bbox_inches='tight')
    plt.close(fig)
    
    return output
