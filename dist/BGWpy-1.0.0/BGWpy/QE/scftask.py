from __future__ import print_function
import os

from . import QETask
from . import get_scf_input


class ScfTask(QETask):
    """Charge density calculation."""

    def __init__(self, dirname, **kwargs):
        """
        Arguments
        ---------

        dirname : str
            Directory in which the files are written and the code is executed.
            Will be created if needed.


        Keyword arguments
        -----------------
        (All mandatory unless specified otherwise)

        prefix : str
            Prefix required by QE as a rootname.
        pseudo_dir : str
            Directory in which pseudopotential files are found.
        pseudos : list, str
            Pseudopotential files.
        structure : pymatgen.Structure
            Structure object containing information on the unit cell.
        ecutwfc : float
            Energy cutoff for the wavefunctions
        ngkpt : list(3), float, optional
            K-points grid. Number of k-points along each primitive vector
            of the reciprocal lattice.
            K-points are either specified using ngkpt or using kpts and wtks.
        kshift : list(3), float, optional
            Relative shift of the k-points grid along each direction,
            as a fraction of the smallest division along that direction.
        qshift : list(3), float, optional
            Absolute shift of the k-points grid along each direction.
        symkpt : bool (True), optional
            Use symmetries for the k-point grid generation.
        kpts : 2D list(nkpt,3), float, optional
            List of k-points.
            K-points are either specified using ngkpt or using kpts and wtks.
        wtks : list(nkpt), float, optional
            Weights of each k-point.


        Properties
        ----------

        charge_density_fname : str
            Path to the charge density file produced ('charge-density.dat').
        data_file_fname : str
            Path to the xml data file produced ('data-file.xml').
        spin_polarization_fname : str, optional
            Path to the spin polarization file produced ('spin-polarization.dat').
        """

        super(ScfTask, self).__init__(dirname, **kwargs)

        kpts, wtks = self.get_kpts(kwargs)

        # Input file
        self.input = get_scf_input(
            self.prefix,
            self.pseudo_dir,
            kwargs['pseudos'],
            kwargs['structure'],
            kwargs['ecutwfc'],
            kpts,
            wtks,
            )

        self.input.fname = 'scf.in'

        # Run script
        self.runscript['PW'] = 'pw.x'
        self.runscript.append('$MPIRUN $PW -in scf.in &> scf.out')

    @property
    def charge_density_fname(self):
        return os.path.join(self.dirname, self.savedir, 'charge-density.dat')

    @property
    def spin_polarization_fname(self):
        return os.path.join(self.dirname, self.savedir, 'spin-polarization.dat')

    @property
    def data_file_fname(self):
        return os.path.join(self.dirname, self.savedir, 'data-file.xml')

