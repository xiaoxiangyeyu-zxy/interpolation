from scipy.io import FortranFile
import numpy as np
import math

fi = [0]*36
EOSIMAX = 211  # den index
EOSJMAX = 71  # temp index

btemp = 1e07
den = 1e04
abar = 4.0
zbar = 2.0
ye = abar/zbar
print('The temperature is:', "%e" % btemp)
print('The density is:', "%e" % den)
print('den*abar/zbar=', "%e" % (den*ye))

# temp 10**4---10**11   den 10**(-10)---10**11
eos_tlo = 4.e0
tstp = (11.0e0 - eos_tlo)/float(EOSJMAX-1)
eos_tstpi = 1/tstp
eos_dlo = -10.0e0
dstp = (11.0e0 - eos_dlo)/float(EOSIMAX-1)
eos_dstpi = 1/dstp

# store the grid
eos_t = np.zeros(EOSJMAX)
eos_d = np.zeros(EOSIMAX)
for j in range(EOSJMAX):
    eos_t[j] = 10.0e0 ** (eos_tlo + j * tstp)
for i in range(EOSIMAX):
    eos_d[i] = 10.0e0 ** (eos_dlo + i * dstp)

# store the temperature and density differences and their inverses
eos_dt = np.zeros(EOSJMAX-1)
eos_dtSqr = np.zeros(EOSJMAX-1)
eos_dtInv = np.zeros(EOSJMAX-1)
eos_dtSqrInv = np.zeros(EOSJMAX-1)

for j in range(EOSJMAX-1):
    eos_dt[j] = eos_t[j+1] - eos_t[j]
    eos_dtSqr[j] = eos_dt[j]*eos_dt[j]
    eos_dtInv[j] = 1.0e0/eos_dt[j]
    eos_dtSqrInv[j] = 1.0e0/eos_dtSqr[j]

eos_dd = np.zeros(EOSIMAX-1)
eos_ddSqr = np.zeros(EOSIMAX-1)
eos_ddInv = np.zeros(EOSIMAX-1)
eos_ddSqrInv = np.zeros(EOSIMAX-1)

for i in range(EOSIMAX-1):
    eos_dd[i] = eos_d[i+1] - eos_d[i]
    eos_ddSqr[i] = eos_dd[i]*eos_dd[i]
    eos_ddInv[i] = 1.0e0/eos_dd[i]
    eos_ddSqrInv[i] = 1.0e0/eos_ddSqr[i]


# read the table
fii = FortranFile('helm_table.bdat', 'r')
f = fii.read_reals(dtype=float)
fd = fii.read_reals(dtype=float)
ft = fii.read_reals(dtype=float)
fdd = fii.read_reals(dtype=float)
ftt = fii.read_reals(dtype=float)
fdt = fii.read_reals(dtype=float)
fddt = fii.read_reals(dtype=float)
fdtt = fii.read_reals(dtype=float)
fddtt = fii.read_reals(dtype=float)
dpdf = fii.read_reals(dtype=float)
dpdfd = fii.read_reals(dtype=float)
dpdft = fii.read_reals(dtype=float)
dpdfdt = fii.read_reals(dtype=float)
ef = fii.read_reals(dtype=float)
efd = fii.read_reals(dtype=float)
eft = fii.read_reals(dtype=float)
efdt = fii.read_reals(dtype=float)
xf = fii.read_reals(dtype=float)
xfd = fii.read_reals(dtype=float)
xft = fii.read_reals(dtype=float)
xfdt = fii.read_reals(dtype=float)

# f --  Helmholtz free energy
# fd --  derivative of f wrt density
# ft --  derivative of f wrt temperature
# fdd --  second derivative of f wrt density
# ftt --  second derivative of f wrt temperature
# fdt --  second derivative of f wrt density and temperature
# fddt --  third derivative of f wrt density^2 and temperature
# fdtt --  third derivative of f wrt density and temperature^2 e.g. dF/(dd)(dt^2)
# fddtt --  fourth derivative of f wrt density^2 and temperature^2
# dpdf --  pressure derivative
# dpdfd --
# dpdft --
# dpdfdt --
# ef --  electron chemical potential
# efd --
# eft --
# efdt --
# xf --  number density
# xfd --
# xft --
# xfdt --

eos_f = np.zeros((EOSIMAX, EOSJMAX))
eos_fd = np.zeros((EOSIMAX, EOSJMAX))
eos_ft = np.zeros((EOSIMAX, EOSJMAX))
eos_fdd = np.zeros((EOSIMAX, EOSJMAX))
eos_ftt = np.zeros((EOSIMAX, EOSJMAX))
eos_fdt = np.zeros((EOSIMAX, EOSJMAX))
eos_fddt = np.zeros((EOSIMAX, EOSJMAX))
eos_fdtt = np.zeros((EOSIMAX, EOSJMAX))
eos_fddtt = np.zeros((EOSIMAX, EOSJMAX))
eos_dpdf = np.zeros((EOSIMAX, EOSJMAX))
eos_dpdfd = np.zeros((EOSIMAX, EOSJMAX))
eos_dpdft = np.zeros((EOSIMAX, EOSJMAX))
eos_dpdfdt = np.zeros((EOSIMAX, EOSJMAX))
eos_ef = np.zeros((EOSIMAX, EOSJMAX))
eos_efd = np.zeros((EOSIMAX, EOSJMAX))
eos_eft = np.zeros((EOSIMAX, EOSJMAX))
eos_efdt = np.zeros((EOSIMAX, EOSJMAX))
eos_xf = np.zeros((EOSIMAX, EOSJMAX))
eos_xfd = np.zeros((EOSIMAX, EOSJMAX))
eos_xft = np.zeros((EOSIMAX, EOSJMAX))
eos_xfdt = np.zeros((EOSIMAX, EOSJMAX))

for j in range(EOSJMAX):
    for i in range(EOSIMAX):
        eos_f[i, j] = f[j * EOSIMAX + i]
        eos_fd[i, j] = fd[j * EOSIMAX + i]
        eos_ft[i, j] = ft[j * EOSIMAX + i]
        eos_fdd[i, j] = fdd[j * EOSIMAX + i]
        eos_ftt[i, j] = ftt[j * EOSIMAX + i]
        eos_fdt[i, j] = fdt[j * EOSIMAX + i]
        eos_fddt[i, j] = fddt[j * EOSIMAX + i]
        eos_fdtt[i, j] = fdtt[j * EOSIMAX + i]
        eos_fddtt[i, j] = fddtt[j * EOSIMAX + i]
        eos_dpdf[i, j] = dpdf[j * EOSIMAX + i]
        eos_dpdfd[i, j] = dpdfd[j * EOSIMAX + i]
        eos_dpdft[i, j] = dpdft[j * EOSIMAX + i]
        eos_dpdfdt[i, j] = dpdfdt[j * EOSIMAX + i]
        eos_ef[i, j] = ef[j * EOSIMAX + i]
        eos_efd[i, j] = efd[j * EOSIMAX + i]
        eos_eft[i, j] = eft[j * EOSIMAX + i]
        eos_efdt[i, j] = efdt[j * EOSIMAX + i]
        eos_xf[i, j] = xf[j * EOSIMAX + i]
        eos_xfd[i, j] = xfd[j * EOSIMAX + i]
        eos_xft[i, j] = xft[j * EOSIMAX + i]
        eos_xfdt[i, j] = xfdt[j * EOSIMAX + i]

# print(len(eos_f[0]))
# print(eos_f)


# quintic hermite polynomial statement functions
# psi0 and its derivatives
def psi0(zfunc):
    res = zfunc**3 * (zfunc * (-6.0e0 * zfunc + 15.0e0) - 10.0e0) + 1.0e0
    return res


def dpsi0(zfunc):
    res = zfunc**2 * (zfunc * (-30.0e0 * zfunc + 60.0e0) - 30.0e0)
    return res


def ddpsi0(zfunc):
    res = zfunc * (zfunc*(-120.0e0*zfunc + 180.0e0) - 60.0e0)
    return res


# psi1 and its derivatives
def psi1(zfunc):
    res = zfunc * (zfunc**2 * (zfunc * (-3.0e0*zfunc + 8.0e0) - 6.0e0) + 1.0e0)
    return res


def dpsi1(zfunc):
    res = zfunc*zfunc * (zfunc * (-15.0e0*zfunc + 32.0e0) - 18.0e0) + 1.0e0
    return res


def ddpsi1(zfunc):
    res = zfunc * (zfunc * (-60.0e0*zfunc + 96.0e0) - 36.0e0)
    return res


# psi2  and its derivatives
def psi2(zfunc):
    res = 0.5e0*zfunc*zfunc*(zfunc*(zfunc * (-zfunc + 3.0e0) - 3.0e0) + 1.0e0)
    return res


def dpsi2(zfunc):
    res = 0.5e0*zfunc*(zfunc*(zfunc*(-5.0e0*zfunc + 12.0e0) - 9.0e0) + 2.0e0)
    return res


def ddpsi2(zfunc):
    res = 0.5e0*(zfunc*(zfunc * (-20.0e0*zfunc + 36.0e0) - 18.0e0) + 2.0e0)
    return res


# The resulting biquintic interpolation function
def h5(w0t, w1t, w2t, w0mt, w1mt, w2mt, w0d, w1d, w2d, w0md, w1md, w2md):
    res = fi[0]*w0d*w0t + fi[1]*w0md*w0t + fi[2]*w0d*w0mt + fi[3]*w0md*w0mt \
       + fi[4]*w0d*w1t + fi[5]*w0md*w1t + fi[6]*w0d*w1mt + fi[7]*w0md*w1mt \
       + fi[8]*w0d*w2t + fi[9]*w0md*w2t + fi[10]*w0d*w2mt + fi[11]*w0md*w2mt \
       + fi[12]*w1d*w0t + fi[13]*w1md*w0t + fi[14]*w1d*w0mt + fi[15]*w1md*w0mt \
       + fi[16]*w2d*w0t + fi[17]*w2md*w0t + fi[18]*w2d*w0mt + fi[19]*w2md*w0mt \
       + fi[20]*w1d*w1t + fi[21]*w1md*w1t + fi[22]*w1d*w1mt + fi[23]*w1md*w1mt \
       + fi[24]*w2d*w1t + fi[25]*w2md*w1t + fi[26]*w2d*w1mt + fi[27]*w2md*w1mt \
       + fi[28]*w1d*w2t + fi[29]*w1md*w2t + fi[30]*w1d*w2mt + fi[31]*w1md*w2mt \
       + fi[32]*w2d*w2t + fi[33]*w2md*w2t + fi[34]*w2d*w2mt + fi[35]*w2md*w2mt
    return res


# cubic hermite polynomial statement functions
# psi0
def xpsi0(zfunc):
    res = zfunc * zfunc * (2.0e0*zfunc - 3.0e0) + 1.0
    return res


def xpsi1(zfunc):
    res = zfunc * (zfunc * (zfunc - 2.0e0) + 1.0e0)
    return res


din = ye*den
jat = int((math.log10(btemp) - eos_tlo)*eos_tstpi)
jat = max(0, min(jat, EOSJMAX-2))
iat = int((math.log10(din) - eos_dlo)*eos_dstpi)
iat = max(0, min(iat, EOSIMAX-2))
# print(jat)
# print(iat)

fi[0] = eos_f[iat, jat]
fi[1] = eos_f[iat + 1, jat]
fi[2] = eos_f[iat, jat + 1]
fi[3] = eos_f[iat + 1, jat + 1]
fi[4] = eos_ft[iat, jat]
fi[5] = eos_ft[iat + 1, jat]
fi[6] = eos_ft[iat, jat + 1]
fi[7] = eos_ft[iat + 1, jat + 1]
fi[8] = eos_ftt[iat, jat]
fi[9] = eos_ftt[iat + 1, jat]
fi[10] = eos_ftt[iat, jat + 1]
fi[11] = eos_ftt[iat + 1, jat + 1]
fi[12] = eos_fd[iat, jat]
fi[13] = eos_fd[iat + 1, jat]
fi[14] = eos_fd[iat, jat + 1]
fi[15] = eos_fd[iat + 1, jat + 1]
fi[16] = eos_fdd[iat, jat]
fi[17] = eos_fdd[iat + 1, jat]
fi[18] = eos_fdd[iat, jat + 1]
fi[19] = eos_fdd[iat + 1, jat + 1]
fi[20] = eos_fdt[iat, jat]
fi[21] = eos_fdt[iat + 1, jat]
fi[22] = eos_fdt[iat, jat + 1]
fi[23] = eos_fdt[iat + 1, jat + 1]
fi[24] = eos_fddt[iat, jat]
fi[25] = eos_fddt[iat + 1, jat]
fi[26] = eos_fddt[iat, jat + 1]
fi[27] = eos_fddt[iat + 1, jat + 1]
fi[28] = eos_fdtt[iat, jat]
fi[29] = eos_fdtt[iat + 1, jat]
fi[30] = eos_fdtt[iat, jat + 1]
fi[31] = eos_fdtt[iat + 1, jat + 1]
fi[32] = eos_fddtt[iat, jat]
fi[33] = eos_fddtt[iat + 1, jat]
fi[34] = eos_fddtt[iat, jat + 1]
fi[35] = eos_fddtt[iat + 1, jat + 1]

# various differences
xt = max((btemp - eos_t[jat])*eos_dtInv[jat], 0.0e0)
xd = max((din - eos_d[iat]) * eos_ddInv[iat], 0.0e0)
mxt = 1.0e0 - xt
mxd = 1.0e0 - xd

# the density and temperature basis functions
si0t = psi0(xt)
si1t = psi1(xt) * eos_dt[jat]
si2t = psi2(xt) * eos_dtSqr[jat]

si0mt = psi0(mxt)
si1mt = -psi1(mxt) * eos_dt[jat]
si2mt = psi2(mxt) * eos_dtSqr[jat]

si0d = psi0(xd)
si1d = psi1(xd) * eos_dd[iat]
si2d = psi2(xd) * eos_ddSqr[iat]

si0md = psi0(mxd)
si1md = -psi1(mxd) * eos_dd[iat]
si2md = psi2(mxd) * eos_ddSqr[iat]

# the first derivatives of the basis functions
dsi0t = dpsi0(xt) * eos_dtInv[jat]
dsi1t = dpsi1(xt)
dsi2t = dpsi2(xt) * eos_dt[jat]

dsi0mt = -dpsi0(mxt) * eos_dtInv[jat]
dsi1mt = dpsi1(mxt)
dsi2mt = -dpsi2(mxt) * eos_dt[jat]

dsi0d = dpsi0(xd) * eos_ddInv[iat]
dsi1d = dpsi1(xd)
dsi2d = dpsi2(xd) * eos_dd[iat]

dsi0md = -dpsi0(mxd) * eos_ddInv[iat]
dsi1md = dpsi1(mxd)
dsi2md = -dpsi2(mxd) * eos_dd[iat]

# the second derivatives of the basis functions
ddsi0t = ddpsi0(xt) * eos_dtSqrInv[jat]
ddsi1t = ddpsi1(xt) * eos_dtInv[jat]
ddsi2t = ddpsi2(xt)

ddsi0mt = ddpsi0(mxt) * eos_dtSqrInv[jat]
ddsi1mt = -ddpsi1(mxt) * eos_dtInv[jat]
ddsi2mt = ddpsi2(mxt)


# the free energy
free = h5(si0t, si1t, si2t, si0mt, si1mt, si2mt, si0d, si1d, si2d, si0md, si1md, si2md)
print('The free energy is:', '%.16e' % free)

# derivative with respect to density
df_d = h5(si0t, si1t, si2t, si0mt, si1mt, si2mt, dsi0d, dsi1d, dsi2d, dsi0md, dsi1md, dsi2md)

# derivative with respect to temperature
df_t = h5(dsi0t, dsi1t, dsi2t, dsi0mt, dsi1mt, dsi2mt, si0d, si1d, si2d, si0md, si1md, si2md)

# second derivative with respect to temperature
df_tt = h5(ddsi0t, ddsi1t, ddsi2t, ddsi0mt, ddsi1mt, ddsi2mt, si0d, si1d, si2d, si0md, si1md, si2md)

# second derivative with respect to temperature and density
df_dt = h5(dsi0t, dsi1t, dsi2t, dsi0mt, dsi1mt, dsi2mt, dsi0d, dsi1d, dsi2d, dsi0md, dsi1md, dsi2md)

# df_dd = h5(si0t, si1t, si2t, si0mt, si1mt, si2mt, ddsi0d, ddsi1d, ddsi2d, ddsi0md, ddsi1md, ddsi2md)

# the desired electron - positron thermodynamic quantities
x3 = din * din
pele = x3 * df_d  # pressure p
dpepdt = x3 * df_dt  # dp/dt
# dpepdd = ye * (din**2 * df_dd + 2.0d0 * din * df_d)

sele = -df_t * ye  # entropy s
dsepdt = -df_tt * ye  # ds/dt
dsepdd = -df_dt * ye * ye  # ds/dd

eele = ye * free + btemp * sele  # internal energy e
deepdt = btemp * dsepdt  # de/dt
deepdd = ye * ye * df_d + btemp * dsepdd  # de/dd

print('The presssure is:', '%.16e' % pele)
print('The entropy is:', '%.16e' % sele)
print('The internal energy is:', '%.16e' % eele)
