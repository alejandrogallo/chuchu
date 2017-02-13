// File produced automatically by chuchu program
// https://github.com/alejandrogallo/chuchu

// include asy_atoms from a specific path
include "$asy_atom";
// or import it from your system
//import atoms;

unitsize(1cm);

//currentprojection  = perspective(1,1,1);
settings.prc         = false;
settings.render      = 10; //quality
//settings.outformat = "pdf";

real bond_radius   = $bond_radius;
real radius_scale  = $radius_scale;
real max_bond_dist = $max_length;
real min_bond_dist = $min_length;
currentlight       = AtomLight;

$camera

Basis basis = Basis();
    $basis
); //This basis has been already scaled up



$atoms



$draw_atoms



$draw_bonds

