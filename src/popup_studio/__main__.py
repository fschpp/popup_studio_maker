from __future__ import annotations

import argparse

from popup_studio import __version__
from popup_studio.mechanisms.step_fold import StepFold


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="popup-studio")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="cmd")
    sf = sub.add_parser("step-fold", help="tabla de la sección transversal del step-fold")
    sf.add_argument("--h", type=float, default=40.0)
    sf.add_argument("--g", type=float, default=40.0)
    ex = sub.add_parser("export-step", help="PDF del patrón del step-fold (1:1)")
    ex.add_argument("--h", type=float, default=40.0)
    ex.add_argument("--g", type=float, default=40.0)
    ex.add_argument("--width", type=float, default=60.0)
    ex.add_argument("-o", "--output", default="step_fold.pdf")
    sub.add_parser("calibration", help="PDF de calibración con cuadrado de 100 mm")
    sub.add_parser("gui", help="abrir la ventana (requiere GTK 4)")
    args = p.parse_args(argv)
    if args.cmd == "export-step":
        from popup_studio.export.pdf import export_patterns
        from popup_studio.layout.step_fold_layout import step_fold_pattern

        export_patterns([step_fold_pattern(StepFold(args.h, args.g), args.width)], args.output)
        print(f"escrito {args.output}")
        return 0
    if args.cmd == "calibration":
        from popup_studio.export.pdf import export_calibration

        export_calibration("00_calibracion.pdf")
        print("escrito 00_calibracion.pdf")
        return 0
    if args.cmd == "gui":
        from popup_studio.ui.app import run

        return run()
    if args.cmd == "step-fold":
        s = StepFold(args.h, args.g)
        print("phi    A(y,z)              M(y,z)")
        for phi in (0, 45, 90, 135, 180):
            sec = s.cross_section(phi)
            print(f"{phi:>3}°  {sec['A'][0]:8.2f},{sec['A'][1]:7.2f}   "
                  f"{sec['M'][0]:8.2f},{sec['M'][1]:7.2f}")
        return 0
    p.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
