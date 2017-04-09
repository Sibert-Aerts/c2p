from .base import PInstruction

from .arithmetic import Add, Sub, Mul, Div, Neg, Inc, Dec
from .array import Ixa, Chk, Dpl, Ldd, Sli
from .branch import Ujp, Fjp, Ixj, Label
from .comparison import Equ, Geq, Leq, Les, Grt, Neq
from .io import In, Out1, Out2
from .logic import And, Or, Not
from .misc import New, Hlt, Conv, Movs, Movd
from .procedure import Mst, Cup, Ssp, Sep, Ent, Retf, Retp, Smp, Cupi, Mstf
from .store_load import Ldo, Ldc, Ind, Sro, Sto, Lod, Lda, Str
