import numpy as np
from scipy.interpolate import splev, splrep, splint, interp1d
from MDSplus import *

class Signals:

    def __init__(self, shot):
        """
        Imports signals from MDSplus
        :param shot: experimental pulse number
        """

        self.shot = shot
        self.conn = Connection('192.168.1.7:8000')
        self.conn.openTree('st40', self.shot)

    def cxrs_tws_c_ti_spectra(self, t):
        """
        Ion temperature profile from TriWaSp CXRS C line
        :param t:
        :return:
        """

        s = '.CXFF_TWS_C.BEST:SPECTRA'
        path_dim = f'dim_of({s},{0})'
        no = self.conn.get(path_dim).data()
        r = self.conn.get(f'dim_of({s},{1})').data()
        time = self.conn.get(f'dim_of({s},{2})').data()
        data = self.conn.get(s).data()
        err = self.conn.get('.CXFF_TWS_C.BEST:SPECTRA_ERR').data()
        #wavel = self.conn.get('.CXFF_TWS_C.BEST.PROFILES:L_WAVE').data()
        i0 = np.argmin(abs(time - t[0]))
        i1 = np.argmin(abs(time - t[1]))

        return time[i0:i1], r, data[i0:i1], err[i0:i1]

    def cxrs_tws_c_ti(self, t):
        """
        Ion temperature profile from TriWaSp CXRS C line
        :param t:
        :return:
        """

        s = '.CXFF_TWS_C.BEST.PROFILES:TI'
        path_dim = f'dim_of({s},{0})'
        r = self.conn.get(path_dim).data()
        time = self.conn.get(f'dim_of({s},{1})').data()
        data = self.conn.get(s).data()
        err = self.conn.get('.CXFF_TWS_C.BEST.PROFILES:TI_ERR').data()
        i0 = np.argmin(abs(time - t[0]))
        i1 = np.argmin(abs(time - t[1]))

        return time[i0:i1], r, data[i0:i1]*1e-3, err[i0:i1]*1e-3

    def cxrs_tws_c_vtor(self, t):
        """
        Vtor profile from TriWaSp CXRS C line
        :param t:
        :return:
        """
        s = '.CXFF_TWS_C.BEST.PROFILES:VTOR'
        path_dim = f'dim_of({s},{0})'
        r = self.conn.get(path_dim).data()
        time = self.conn.get(f'dim_of({s},{1})').data()
        data = self.conn.get(s).data()
        err = self.conn.get('.CXFF_TWS_C.BEST.PROFILES:VTOR_ERR').data()
        i0 = np.argmin(abs(time - t[0]))
        i1 = np.argmin(abs(time - t[1]))

        return time[i0:i1], r, data[i0:i1], err[i0:i1]

    def cxrs_pi_ti(self, t):
        """
        Ion temperature profile from PI CX
        :param t:
        :return:
        """

        s = '.CXFF_PI.BEST.PROFILES:TI'
        path_dim = f'dim_of({s},{0})'
        r = self.conn.get(path_dim).data()
        time = self.conn.get(f'dim_of({s},{1})').data()
        data = self.conn.get(s).data()
        err = self.conn.get('.CXFF_PI.BEST.PROFILES:TI_ERR').data()
        i0 = np.argmin(abs(time - t[0]))
        i1 = np.argmin(abs(time - t[1]))

        return time[i0:i1], r, data[i0:i1]*1e-3, err[i0:i1]*1e-3

    def cxrs_pi_vtor(self, t):
        """
        Vtor profile from PI CX
        :param t:
        :return:
        """
        s = '.CXFF_PI.BEST.PROFILES:VTOR'
        path_dim = f'dim_of({s},{0})'
        r = self.conn.get(path_dim).data()
        time = self.conn.get(f'dim_of({s},{1})').data()
        data = self.conn.get(s).data()
        err = self.conn.get('.CXFF_PI.BEST.PROFILES:VTOR_ERR').data()
        i0 = np.argmin(abs(time - t[0]))
        i1 = np.argmin(abs(time - t[1]))

        return time[i0:i1], r, data[i0:i1], err[i0:i1]

    def thomson_nel_smm(self, t):
        """
        Line integrated ne from TS data (Z=0)
        :param t:
        :return:
        """
        s = '.TS.BEST.GLOBAL:SMM_NEL'
        path_dim = f"dim_of({s},{0})"
        time = self.conn.get(path_dim).data()
        nel_ts = self.conn.get(s).data()
        i0 = np.argmin(abs(time - t[0]))
        i1 = np.argmin(abs(time - t[1]))

        return time[i0:i1], nel_ts[i0:i1]

    def thomson_ne_profile(self, t):

        s = '.TS.BEST.PROFILES:NE'
        path_dim = f'dim_of({s},{0})'
        r = self.conn.get(path_dim).data()
        time = self.conn.get(f'dim_of({s},{1})').data()
        ne = self.conn.get(s).data()
        ne_err = self.conn.get('.TS.BEST.PROFILES:NE_ERR').data()
        i0 = np.argmin(abs(time - t[0]))
        i1 = np.argmin(abs(time - t[1]))

        return time[i0:i1], r, ne[i0:i1], ne_err[i0:i1]

    def thomson_te_profile(self, t):

        s = '.TS.BEST.PROFILES:TE'
        path_dim = f'dim_of({s},{0})'
        r = self.conn.get(path_dim).data()
        time = self.conn.get(f'dim_of({s},{1})').data()
        te = self.conn.get(s).data()
        te_err = self.conn.get('.TS.BEST.PROFILES:TE_ERR').data()
        i0 = np.argmin(abs(time - t[0]))
        i1 = np.argmin(abs(time - t[1]))

        return time[i0:i1], r, te[i0:i1], te_err[i0:i1]

    def ts_smooth(self,t,smooth_factor_ne=2,smooth_factor_te=0.5, dr=0.02):

        # --- TS ne profile --- #
        time_ts, r, ne, ne_err = self.thomson_ne_profile(t)

        # --- TS Te profile --- #
        _, _, te, te_err = self.thomson_te_profile(t)

        ir_sort = np.argsort(r)
        r_sort = r[ir_sort]
        ne_sort = ne[:, ir_sort] * 1e-19
        ne_err_sort = ne_err[:, ir_sort] * 1e-19
        te_sort = te[:, ir_sort] * 1e-3
        te_err_sort = te_err[:, ir_sort] * 1e-3

        inan = np.logical_not(np.isnan(ne_sort))

        ne_smooth = []
        te_smooth = []
        r_smooth = []  #[] for i in range(ne_sort.shape[0])]

        for i in range(ne_sort.shape[0]):
            ne_n = ne_sort[i, inan[i]]
            te_n = te_sort[i, inan[i]]
            ne_err_n = ne_err_sort[i, inan[i]]
            te_err_n = te_err_sort[i, inan[i]]
            r_n = r_sort[inan[i]]
            s = ne_n.shape[0] - np.sqrt(2 * ne_n.shape[0])

            x_new = np.arange(np.min(r_n), np.max(r_n), dr)

            tck_ne = splrep(r_n, ne_n, w=1.0 / ne_err_n, s=smooth_factor_ne * s, full_output=True)
            tck_te = splrep(r_n, te_n, w=1.0 / te_err_n, s=smooth_factor_te * s, full_output=True)
            ne_sm = splev(x_new, tck_ne[0], ext=1)
            te_sm = splev(x_new, tck_te[0], ext=1)
            # checking ne > 0
            ine = ne_sm > 0
            ne_p = ne_sm[ine]
            te_p = te_sm[ine]
            r_p = x_new[ine]
            # checking te > 0
            ite = te_p > 0
            ne_p = ne_p[ite]
            te_p = te_p[ite]
            r_p = r_p[ite]
            ne_smooth.append(ne_p)
            te_smooth.append(te_p)
            r_smooth.append(r_p)

        return time_ts, r_smooth, ne_smooth, te_smooth

    def number_argon_atoms(self, t):
        t0 = t[0]
        t1 = t[1]

        s = 'GAS.BEST.GLOBAL:N_TOTAL_AR'

        path_dim = f"dim_of({s},{0})"
        time = self.conn.get(path_dim).data()
        nar = self.conn.get(s).data()
        idw = np.argmin(abs(time - t0))
        iup = np.argmin(abs(time - t1))

        return time[idw:iup], nar[idw:iup]

    def rate_argon_puff(self, t):
        t0 = t[0]
        t1 = t[1]

        s = 'GAS.BEST.GLOBAL:N_TOTAL_AR'

        path_dim = f"dim_of({s},{0})"
        time = self.conn.get(path_dim).data()
        nar = self.conn.get(s).data()
        idw = np.argmin(abs(time - t0))
        iup = np.argmin(abs(time - t1))

        n_ar1 = nar.copy()
        n_ar1[nar < 0] = 0

        rate = np.diff(n_ar1)
        time_rate = time[:-1] + np.diff(time) / 2

        return time_rate[idw:iup], rate[idw:iup]

    def w_dia(self, t):

        t0 = t[0]
        t1 = t[1]

        s = '.DIALOOP.BEST.GLOBAL:WDIA'

        path_dim = f"dim_of({s},{0})"
        time = self.conn.get(path_dim).data()
        wdia = self.conn.get(s).data()
        idw = np.argmin(abs(time - t0))
        iup = np.argmin(abs(time - t1))

        return time[idw:iup], wdia[idw:iup]

    def sxr(self, t):
        """
        Imports signal from a single SXR AXUV diode [W/m^2]
         ?10 mkm Be foil, 50 mkm Si diode thickness?
         etendue = 6.76e-9 m^2, S=0.26 A/W  {from Sundar S }
        :param t: [t_start, t_end]
        :return: time_vector, signal in kW/m^2
        """

        t0 = t[0]
        t1 = t[1]

        s = 'SXR.DIODE_DETR.BEST.FILTER_001:SIGNAL'
        path_dim = f"dim_of({s},{0})"
        time = self.conn.get(path_dim).data()
        INTSXR = self.conn.get(s).data()
        idw = np.argmin(abs(time - t0))
        iup = np.argmin(abs(time - t1))

        timesxr = time[idw:iup]
        isxr = INTSXR[idw:iup]
        print('units:',self.conn.get('UNITS_OF(SXR.DIODE_DETR.BEST.FILTER_001:SIGNAL)'))

        return timesxr, isxr*1e-3

    def sxr_emissivity(self, t):
        """
        Imports signal from a single SXR AXUV diode [W/m^2]
         ?10 mkm Be foil, 50 mkm Si diode thickness?
         etendue = 6.76e-9 m^2, S=0.26 A/W  {from Sundar S }
        :param t: [t_start, t_end]
        :return: time_vector, signal in kW/m^2
        """

        t0 = t[0]
        t1 = t[1]

        s = 'SXR_SPD.BEST.GLOBAL:EMISSION_1'
        path_dim = f"dim_of({s},{0})"
        time = self.conn.get(path_dim).data()
        INTSXR = self.conn.get(s).data()
        idw = np.argmin(abs(time - t0))
        iup = np.argmin(abs(time - t1))

        timesxr = time[idw:iup]
        isxr = INTSXR[idw:iup]
        print('units:',self.conn.get('UNITS_OF(SXR.DIODE_DETR.BEST.FILTER_001:SIGNAL)'))

        return timesxr, isxr*1e-3

    def halpha(self, t):
        """
        H_alpha signal measured by a line diode PDA36A - EC(60 dB)
        Midplane geometry
        wavelength range = 656.28+/-5nm
        :param t:
        :return: time, signal in Volts, signal in Watts
        """

        etendue = 3.4e-7          # m2 sr
        transm = 0.89
        gain = 1.5e6              # V/A
        sensitivity = 0.3405      # A/W

        t0 = t[0]
        t1 = t[1]

        s = 'SPECTROM.LINES.H_ALPHA_MP1:INTENSITY'
        path_dim = f"dim_of({s},{0})"
        time = self.conn.get(path_dim).data()
        intha = self.conn.get(s).data()
        idw = np.argmin(abs(time - t0))
        iup = np.argmin(abs(time - t1))

        print('units:', self.conn.get('UNITS_OF(SPECTROM.LINES.H_ALPHA_MP1:INTENSITY)'))

        power = intha / gain / sensitivity / etendue / transm  # W/m2

        return time[idw:iup], intha[idw:iup], power[idw:iup]

    def brems_abs(self, t):
        """
        Bremsstrahlung power
        Detector PDA36A-EC (70dB), filter TL FL532-10&FB540-10
        wavelength l~536+/-2nm
        Uses absolute calibration measured in a lab by H.W.
        :param t:
        :return:
        """

        t0 = t[0]
        t1 = t[1]

        signame = 'SPECTROM.LINES.BEST.BREM_MP1:EMISSION'
        signame_err = 'SPECTROM.LINES.BEST.BREM_MP1:EMISSION_ERR'
        path_dim = f"dim_of({signame},{0})"
        time = self.conn.get(path_dim).data()
        brem = self.conn.get(signame).data()
        err = self.conn.get(signame_err).data()

        iup = np.argmin(abs(time - t1))
        idw = np.argmin(abs(time - t0))

        print('units:', self.conn.get('UNITS_OF(SPECTROM.LINES.BEST.BREM_MP1:EMISSION)'))

        return time[idw:iup], brem[idw:iup], err[idw:iup]

    def brems(self, t):
        """
        Bremsstrahlung power
        Detector PDA36A-EC (70dB), filter TL FL532-10&FB540-10
        Wavelegnth l~536+/-2nm
        Uses a nominal calibration from manufacturer
        Lab calibration (transmittance and sensitivity) is under tree SPECTROM.LINES/ABS_CALIB
        :param t: [start time, end time]
        :return: time vector, signal in V, signal in W/m^2
        """

        etendue = 3.4e-7           # m2 sr
        transm = 0.36
        gain = 4.75e6              # V/A
        sensitivity = 0.206        # A/W

        t0 = t[0]
        t1 = t[1]

        signame = 'SPECTROM.LINES.BREM_MP1:INTENSITY'
        path_dim = f"dim_of({signame},{0})"
        time = self.conn.get(path_dim).data()
        intbrem = self.conn.get(signame).data()
        iup = np.argmin(abs(time - t1))
        idw = np.argmin(abs(time - t0))

        power = 4*np.pi*intbrem / gain / sensitivity / etendue / transm  # W/m2

        print('units:', self.conn.get('UNITS_OF(SPECTROM.LINES.BREM_MP1:INTENSITY)'))

        return time[idw:iup], intbrem[idw:iup], power[idw:iup]

    def ciii_heii_4647(self, t):
        """
        CIII (+ HeII) line from a photodiode, l=464.7 +/- 5 nm, BW=10 nm
        PDA36A-EC, filter EO 39-315
        :param t:
        :return:
        """
        etendue = 3.4e-7      # m2 sr
        transm = 0.92
        gain = 4.75e6         # V/A
        sensitivity = 0.1295  # A/W

        t0 = t[0]
        t1 = t[1]

        signame = 'SPECTROM.LINES.C3_MP1:INTENSITY'
        path_dim = f"dim_of({signame},{0})"
        time = self.conn.get(path_dim).data()
        intciii = self.conn.get(signame).data()
        iup = np.argmin(abs(time - t1))
        idw = np.argmin(abs(time - t0))

        power = intciii / gain / sensitivity / etendue / transm  # W/m2
        print('units:',self.conn.get('UNITS_OF(SPECTROM.LINES.C3_MP1:INTENSITY)'))
        return time[idw:iup], intciii[idw:iup], power[idw:iup]

    def ciii_4647(self, t):
        """
        CIII line from Avantes spectrometer at 464.7 nm
        :param t:
        :return:
        """

        t0 = t[0]
        t1 = t[1]

        signame04 = '\SPECTROM::TOP.AVANTES.LINE_MON.BEST.LINE_EVOL.C_III_4647:INTENSITY'
        path_dim = f"dim_of({signame04},{0})"
        time = self.conn.get(path_dim).data()
        intciii = self.conn.get(signame04).data()
        iup = np.argmin(abs(time - t1))
        idw = np.argmin(abs(time - t0))
        timeciii = time[idw:iup]
        iciii = intciii[idw:iup]

        return timeciii, iciii

    def ciii_465(self, t):
        """
        CIII 464.7 nm line from Avantes spectrometer
        :param t: [t_start, t_end]
        :return: time, signal
        """

        t0 = t[0]
        t1 = t[1]

        signame04 = '\SPECTROM::TOP.AVANTES.LINE_MON.BEST.LINES:LINES_INT'
        path_dim = f"dim_of({signame04},{1})"   # 0 dimension - names of the lines
        time = self.conn.get(path_dim).data()
        int = self.conn.get(signame04).data()
        intciii_465 = int[:, 85]
        iup = np.argmin(abs(time - t1))
        idw = np.argmin(abs(time - t0))

        return time[idw:iup], intciii_465[idw:iup]

    def cv_227(self, t):
        """
        CV 227 nm line from Avantes spectrometer
        :param t: [t_start, t_end]
        :return: time, signal
        """

        t0 = t[0]
        t1 = t[1]

        signame04 = '\SPECTROM::TOP.AVANTES.LINE_MON.BEST.LINE_EVOL.C_V_2271:INTENSITY'
        cv = self.conn.get(signame04).data()
        path_dim = f"dim_of({signame04},{0})"
        time = self.conn.get(path_dim).data()
        iup = np.argmin(abs(time - t1))
        idw = np.argmin(abs(time - t0))

        return time[idw:iup], cv[idw:iup]

    def arii_465(self, t):
        """
        Ar 465 nm line from Avantes spectrometer
        :param t: [t_start, t_end]
        :return: time, signal
        """

        t0 = t[0]
        t1 = t[1]

        signame04 = '\SPECTROM::TOP.AVANTES.LINE_MON.BEST.LINES:LINES_INT'
        path_dim = f"dim_of({signame04},{1})"   # 0 dimension - names of the lines
        time = self.conn.get(path_dim).data()
        int = self.conn.get(signame04).data()
        intciii_465 = int[:, 43]
        iup = np.argmin(abs(time - t1))
        idw = np.argmin(abs(time - t0))

        return time[idw:iup], intciii_465[idw:iup]

    def uloop(self, t):
        """
        Uloop from L016
        :param t: [t_start, t_end]
        :return: time, signal
        """

        t0 = t[0]
        t1 = t[1]

        signame = '.MAG.BEST.FLOOP.L016:V'
        path_dim = f"dim_of({signame},{0})"
        time = self.conn.get(path_dim).data()
        ul = self.conn.get(signame).data()
        iup = np.argmin(abs(time - t1))
        idw = np.argmin(abs(time - t0))

        return time[idw:iup], ul[idw:iup]

    def ne_smm_avg(self, t):
        """
        NE line averaged from SMM
        :param t: [t_start, t_end]
        :return: time, signal
        """

        t0 = t[0]
        t1 = t[1]

        signame = '.SMMH.BEST.GLOBAL:NE_AVG'
        path_dim = f"dim_of({signame},{0})"
        time = self.conn.get(path_dim).data()
        ne = self.conn.get(signame).data()
        iup = np.argmin(abs(time - t1))
        idw = np.argmin(abs(time - t0))

        return time[idw:iup], ne[idw:iup] * 1e-19

    def ne_smm_int(self, t):
        """
        NE line integrated from SMM
        :param t: [t_start, t_end]
        :return: time, signal
        """

        t0 = t[0]
        t1 = t[1]

        signame = '.SMMH.BEST.GLOBAL:NE_INT'
        path_dim = f"dim_of({signame},{0})"
        time = self.conn.get(path_dim).data()
        ne = self.conn.get(signame).data()
        iup = np.argmin(abs(time - t1))
        idw = np.argmin(abs(time - t0))

        return time[idw:iup], ne[idw:iup]*1e-19

    def ne_smm(self, t):
        """
        NE
        :param t: [t_start, t_end]
        :return: time, signal
        """

        t0 = t[0]
        t1 = t[1]

        signame = '.INTERFEROM.SMMH1.BEST.LINE_AV:NE'
        path_dim = f"dim_of({signame},{0})"
        time = self.conn.get(path_dim).data()
        ne = self.conn.get(signame).data()
        iup = np.argmin(abs(time - t1))
        idw = np.argmin(abs(time - t0))

        return time[idw:iup], ne[idw:iup]*1e-19

    def ne_nir(self, t):
        """
        NE NIR Interferometer
        :param t: [t_start, t_end]
        :return: time, signal
        """

        t0 = t[0]
        t1 = t[1]

        signame = '.INTERFEROM.NIRH1.BEST.LINE_AV:NE'
        path_dim = f"dim_of({signame},{0})"
        time = self.conn.get(path_dim).data()
        ne = self.conn.get(signame).data()
        iup = np.argmin(abs(time - t1))
        idw = np.argmin(abs(time - t0))

        return time[idw:iup], ne[idw:iup]*1e-19

    def int_w(self, t):
        """
        intensity of w-line
        :param t: [t_start, t_end]
        :return: time, signal
        """

        t0 = t[0]
        t1 = t[1]

        signamet = '.SXR.XRCS.BEST:TIME'
        signame = '.SXR.XRCS.BEST.TE_KW:INT_W'

        time = self.conn.get(signamet).data()
        int_w = self.conn.get(signame).data()

        iup = np.argmin(abs(time - t1))
        idw = np.argmin(abs(time - t0))

        return time[idw:iup], int_w[idw:iup]

    def ti0_kw(self, t, core_approx=False):
        """
        Ti0 XRCS KW
        :param t: [t_start, t_end]
        :return: time, signal
        """

        t0 = t[0]
        t1 = t[1]

        signamet = '.SXR.XRCS.BEST:TIME'
        if core_approx:
            signame = '.SXR.XRCS.BEST.TE_KW:TI0'
            signame_err = '.SXR.XRCS.BEST.TE_KW:TI0_ERR'
        else:
            signame = '.SXR.XRCS.BEST.TE_KW:TI'
            signame_err = '.SXR.XRCS.BEST.TE_KW:TI_ERR'

        time = self.conn.get(signamet).data()
        ti0 = self.conn.get(signame).data()
        ti0_err = self.conn.get(signame_err).data()

        iup = np.argmin(abs(time - t1))
        idw = np.argmin(abs(time - t0))

        return time[idw:iup], ti0[idw:iup]*1e-3, ti0_err[idw:iup]*1e-3

    def te0_kw(self, t, core_approx=False):
        """
        Te0 XRCS KW
        :param t: [t_start, t_end]
        :return: time, signal
        """

        t0 = t[0]
        t1 = t[1]

        signamet = '.SXR.XRCS.BEST:TIME'
        if core_approx:
            signame = '.SXR.XRCS.BEST.TE_KW:TE0'
            signame_err = '.SXR.XRCS.BEST.TE_KW:TE0_ERR'
        else:
            signame = '.SXR.XRCS.BEST.TE_KW:TE'
            signame_err = '.SXR.XRCS.BEST.TE_KW:TE_ERR'

        time = self.conn.get(signamet).data()
        te0 = self.conn.get(signame).data()
        te0_err = self.conn.get(signame_err).data()

        iup = np.argmin(abs(time - t1))
        idw = np.argmin(abs(time - t0))

        return time[idw:iup], te0[idw:iup]*1e-3, te0_err[idw:iup]*1e-3

    def ti0_n3w(self, t, core_approx=False):
        """
        Ti0 XRCS N3W
        :param t: [t_start, t_end]
        :return: time, signal
        """

        t0 = t[0]
        t1 = t[1]

        signamet = '.SXR.XRCS.BEST:TIME'
        if core_approx:
            signame = '.SXR.XRCS.BEST.TE_N3W:TI0'
            signame_err = '.SXR.XRCS.BEST.TE_N3W:TI0_ERR'
        else:
            signame = '.SXR.XRCS.BEST.TE_N3W:TI'
            signame_err = '.SXR.XRCS.BEST.TE_N3W:TI_ERR'

        time = self.conn.get(signamet).data()
        ti0 = self.conn.get(signame).data()
        ti0_err = self.conn.get(signame_err).data()

        iup = np.argmin(abs(time - t1))
        idw = np.argmin(abs(time - t0))

        return time[idw:iup], ti0[idw:iup]*1e-3, ti0_err[idw:iup]*1e-3

    def te0_n3w(self, t, core_approx=False):
        """
        Te0 XRCS N3W
        :param t: [t_start, t_end]
        :return: time, signal
        """

        t0 = t[0]
        t1 = t[1]

        signamet = '.SXR.XRCS.BEST:TIME'

        if core_approx:
            signame = '.SXR.XRCS.BEST.TE_N3W:TE0'
            signame_err = '.SXR.XRCS.BEST.TE_N3W:TE0_ERR'
        else:
            signame = '.SXR.XRCS.BEST.TE_N3W:TE'
            signame_err = '.SXR.XRCS.BEST.TE_N3W:TE_ERR'

        time = self.conn.get(signamet).data()
        te0 = self.conn.get(signame).data()
        te0_err = self.conn.get(signame_err).data()

        iup = np.argmin(abs(time - t1))
        idw = np.argmin(abs(time - t0))

        return time[idw:iup], te0[idw:iup]*1e-3, te0_err[idw:iup]*1e-3

    def wp(self, t):
        """
        energy content from EFIT BEST
        :param t: [t_start, t_end]
        :return: time, signal
        """

        t0 = t[0]
        t1 = t[1]

        signamet = '.EFIT.BEST:TIME'
        signame = '.EFIT.BEST.VIRIAL:WP'

        time = self.conn.get(signamet).data()
        wp = self.conn.get(signame).data()

        iup = np.argmin(abs(time - t1))
        idw = np.argmin(abs(time - t0))

        return time[idw:iup], wp[idw:iup]*1e-3

    def nbi_rfx(self, t):
        """
        RFX beam power, MW
        :param t: [t_start, t_end]
        :return: time, signal
        """

        t0 = t[0]
        t1 = t[1]

        signame = '.RFX.BEST:POWER'
        path_dim = f"dim_of({signame},{0})"
        sig = self.conn.get(signame).data()
        time = self.conn.get(path_dim).data()
        iup = np.argmin(abs(time - t1))
        idw = np.argmin(abs(time - t0))

        return time[idw:iup], sig[idw:iup]*1e-6

    def nbi_hnbi(self, t):
        """
        HNBI beam power, MW
        :param t: [t_start, t_end]
        :return: time, signal
        """

        t0 = t[0]
        t1 = t[1]

        signame = '.HNBI1.BEST:POWER'
        path_dim = f"dim_of({signame},{0})"
        sig = self.conn.get(signame).data()
        time = self.conn.get(path_dim).data()
        iup = np.argmin(abs(time - t1))
        idw = np.argmin(abs(time - t0))

        return time[idw:iup], sig[idw:iup]*1e-6

    def ne_nir(self, t):
        """
        ne from NIR
        :param t: [t_start, t_end]
        :return: time, signal
        """
        nenir = self.conn.get('INTERFEROM.NIRH1.BEST.LINE_AV:NE').data()
        time = self.conn.get('INTERFEROM.NIRH1.BEST:TIME').data()
        idw = np.argmin(abs(time - t[0]))
        iup = np.argmin(abs(time - t[1]))

        return time[idw:iup], nenir[idw:iup]

    def gas_puff_total(self, t):
        sig = self.conn.get('.GAS.PUFF_VALVE:GAS_TOTAL').data()

        path_dim = f"dim_of({'.GAS.PUFF_VALVE:GAS_TOTAL'},{0})"
        time = self.conn.get(path_dim).data()

        idw = np.argmin(abs(time - t[0]))
        iup = np.argmin(abs(time - t[1]))

        return time[idw:iup], sig[idw:iup]

    def gas_puff_13(self, t):
        sig = self.conn.get('.GAS.PUFF_VALVE:GAS13_DIAG1').data()

        path_dim = f"dim_of({'.GAS.PUFF_VALVE:GAS13_DIAG1'},{0})"
        time = self.conn.get(path_dim).data()

        idw = np.argmin(abs(time - t[0]))
        iup = np.argmin(abs(time - t[1]))

        return time[idw:iup], sig[idw:iup]

    def gas_puff_14(self, t):
        sig = self.conn.get('.GAS.PUFF_VALVE:GAS14_DIAG2').data()

        path_dim = f"dim_of({'.GAS.PUFF_VALVE:GAS14_DIAG2'},{0})"
        time = self.conn.get(path_dim).data()

        idw = np.argmin(abs(time - t[0]))
        iup = np.argmin(abs(time - t[1]))

        return time[idw:iup], sig[idw:iup]

    def argon_pressure(self, t):
        sig = self.conn.get('.GAS.ION_GAUGE.IVCFIG3:AR_PRESSURE').data()

        path_dim = f"dim_of({'.GAS.ION_GAUGE.IVCFIG3:AR_PRESSURE'},{0})"
        time = self.conn.get(path_dim).data()

        idw = np.argmin(abs(time - t[0]))
        iup = np.argmin(abs(time - t[1]))

        return time[idw:iup], sig[idw:iup]

    def neon_pressure(self, t):
        sig = self.conn.get('.GAS.ION_GAUGE.IVCFIG3:NE_PRESSURE').data()

        path_dim = f"dim_of({'.GAS.ION_GAUGE.IVCFIG3:NE_PRESSURE'},{0})"
        time = self.conn.get(path_dim).data()

        idw = np.argmin(abs(time - t[0]))
        iup = np.argmin(abs(time - t[1]))

        return time[idw:iup], sig[idw:iup]

    def ti_cxrs_passive(self, t):
        sig = self.conn.get('SPECTROM.PRINCETON.PASSIVE.BEST.ION_DOPPLER.TI').data()
        err = self.conn.get('SPECTROM.PRINCETON.PASSIVE.BEST.ION_DOPPLER.DELTA_TI').data()

        path_dim = f"dim_of({'SPECTROM.PRINCETON.PASSIVE.BEST.ION_DOPPLER.TI'},{0})"
        time = self.conn.get(path_dim).data()

        path_dim = f"dim_of({'SPECTROM.PRINCETON.PASSIVE.BEST.ION_DOPPLER.TI'},{1})"
        r = self.conn.get(path_dim).data()

        idw = np.argmin(abs(time - t[0]))
        iup = np.argmin(abs(time - t[1]))

        return time[idw:iup], r, sig[idw:iup], err[idw:iup]

    def v_cxrs_passive(self, t):
        sig = self.conn.get('SPECTROM.PRINCETON.PASSIVE.BEST.ION_DOPPLER.V').data()
        err = self.conn.get('SPECTROM.PRINCETON.PASSIVE.BEST.ION_DOPPLER.DELTA_V').data()

        path_dim = f"dim_of({'SPECTROM.PRINCETON.PASSIVE.BEST.ION_DOPPLER.V'},{0})"
        time = self.conn.get(path_dim).data()

        path_dim = f"dim_of({'SPECTROM.PRINCETON.PASSIVE.BEST.ION_DOPPLER.V'},{1})"
        r = self.conn.get(path_dim).data()

        idw = np.argmin(abs(time - t[0]))
        iup = np.argmin(abs(time - t[1]))

        return time[idw:iup], r, sig[idw:iup], err[idw:iup]

    def ti_cxrs_princeton_best(self, t, runno='BEST'):
        """
        CXSFIT (9619, 9622, 9623, 9624 and 9626)
        Ti keV
        :param t:
        :return:
        """
        sig = self.conn.get(f'SPECTROM.PRINCETON.CXSFIT_OUT.{runno}.TI').data()
        err = self.conn.get(f'SPECTROM.PRINCETON.CXSFIT_OUT.{runno}.TI_ERR').data()

        time = self.conn.get(f'SPECTROM.PRINCETON.CXSFIT_OUT.{runno}.TIME').data()
        r = self.conn.get(f'SPECTROM.PRINCETON.CXSFIT_OUT.{runno}.R').data()

        idw = np.argmin(abs(time - t[0]))
        iup = np.argmin(abs(time - t[1]))

        return time[idw:iup], r, sig[idw:iup]*1e-3, err[idw:iup]*1e-3

    def ti_cxrs_princeton(self, t, runno):
        """
        CXSFIT (9619, 9622, 9623, 9624 and 9626)
        Ti keV
        :param t:
        :param runno:
        :return:
        """
        sig = self.conn.get(f'SPECTROM.PRINCETON.CXSFIT_OUT.RUN{runno}.TI').data()
        err = self.conn.get(f'SPECTROM.PRINCETON.CXSFIT_OUT.RUN{runno}.TI_ERR').data()

        time = self.conn.get(f'SPECTROM.PRINCETON.CXSFIT_OUT.RUN{runno}.TIME').data()
        r = self.conn.get(f'SPECTROM.PRINCETON.CXSFIT_OUT.RUN{runno}.R').data()

        idw = np.argmin(abs(time - t[0]))
        iup = np.argmin(abs(time - t[1]))

        return time[idw:iup], r, sig[idw:iup]*1e-3, err[idw:iup]*1e-3

    def vtor_cxrs_princeton_best(self, t):
        """
        CXSFIT
        Vtor km/s
        :param t:
        :return:
        """
        sig = self.conn.get('SPECTROM.PRINCETON.CXSFIT_OUT.BEST.VTOR').data()
        err = self.conn.get('SPECTROM.PRINCETON.CXSFIT_OUT.BEST.VTOR_ERR').data()

        time = self.conn.get('SPECTROM.PRINCETON.CXSFIT_OUT.BEST.TIME').data()
        r = self.conn.get('SPECTROM.PRINCETON.CXSFIT_OUT.BEST.R').data()

        idw = np.argmin(abs(time - t[0]))
        iup = np.argmin(abs(time - t[1]))

        return time[idw:iup], r, sig[idw:iup]*1e-3, err[idw:iup]*1e-3

    def vtor_cxrs_princeton(self, t, runno):
        """
        CXSFIT
        Vtor km/s
        :param t:
        :param runno:
        :return:
        """
        sig = self.conn.get('SPECTROM.PRINCETON.CXSFIT_OUT.RUN{}.VTOR'.format(runno)).data()
        err = self.conn.get('SPECTROM.PRINCETON.CXSFIT_OUT.RUN{}.VTOR_ERR'.format(runno)).data()

        time = self.conn.get('SPECTROM.PRINCETON.CXSFIT_OUT.RUN{}.TIME'.format(runno)).data()
        r = self.conn.get('SPECTROM.PRINCETON.CXSFIT_OUT.RUN{}.R'.format(runno)).data()

        idw = np.argmin(abs(time - t[0]))
        iup = np.argmin(abs(time - t[1]))

        return time[idw:iup], r, sig[idw:iup]*1e-3, err[idw:iup]*1e-3

    def int_cxrs_princeton(self, t, runno):
        """
        CXSFIT (9619, 9622, 9623, 9624 and 9626)
        :param t:
        :param runno:
        :return:
        """
        sig = self.conn.get('SPECTROM.PRINCETON.CXSFIT_OUT.RUN{}.INT'.format(runno)).data()
        err = self.conn.get('SPECTROM.PRINCETON.CXSFIT_OUT.RUN{}.INT_ERR'.format(runno)).data()

        time = self.conn.get('SPECTROM.PRINCETON.CXSFIT_OUT.RUN{}.TIME'.format(runno)).data()
        r = self.conn.get('SPECTROM.PRINCETON.CXSFIT_OUT.RUN{}.R'.format(runno)).data()

        idw = np.argmin(abs(time - t[0]))
        iup = np.argmin(abs(time - t[1]))

        return time[idw:iup], r, sig[idw:iup], err[idw:iup]

    def exp_cxrs_princeton(self, t, runno):
        """
        CXSFIT (9619, 9622, 9623, 9624 and 9626)
        :param t:
        :param runno:
        :return:
        """
        sig = self.conn.get('SPECTROM.PRINCETON.CXSFIT_OUT.RUN{}.EXPOSURE'.format(runno)).data()
        time = self.conn.get('SPECTROM.PRINCETON.CXSFIT_OUT.RUN{}.TIME'.format(runno)).data()

        idw = np.argmin(abs(time - t[0]))
        iup = np.argmin(abs(time - t[1]))

        return time[idw:iup], sig[idw:iup]
