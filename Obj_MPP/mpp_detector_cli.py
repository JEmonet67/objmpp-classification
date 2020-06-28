#!/usr/bin/env python3

# Copyright CNRS/Inria/UNS
# Contributor(s): Eric Debreuve (since 2018)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import brick.checker as ch_
import brick.config.input_output as cf_
import brick.config.analysis as an_
import brick.config.processing as pc_
import brick.mpp as mp_
import brick.structure.explorer as ex_
from brick.marked_point.generic import marked_point_t
from brick.quality.generic import quality_env_t
from brick.data.type import pl_path_t
from brick.data.config.type import std_label, config_h

import multiprocessing as pl_
import sys as sy_
from typing import Any, Callable, Dict, Optional, Tuple


def RunDetector(
    config: config_h,
    for_deferred_check: config_h,
    ini_document: pl_path_t = None,
    console=sy_.stdout,
    end_character: str = "\n",
) -> Dict[str, Tuple[marked_point_t,...]]:
    #
    import brick.structure.importer as im_

    from datetime import datetime as dt_
    import re as re_

    units = "ymdhmsl"
    start_as_str = re_.sub(
        "[^0-9]", "_", dt_.today().isoformat(sep="+", timespec="milliseconds")
    )
    start_as_str = "".join(
        elm for couple in zip(start_as_str.split("_"), units) for elm in couple
    )

    # --- CONFIGURATION COMPLETION
    #
    if ini_document is None:
        ini_doc_folder = pl_path_t.cwd()
    else:
        ini_doc_folder = ini_document.parent

    has_default_value = pc_.AddDefaultsToConfig(config, {})
    pc_.CanonicalizeTypedConfig(config, ini_doc_folder)

    # --- CONFIGURATION FEEDBACK
    #
    # console_encoding = sy_.stdout.encoding if console == sy_.stdout \
    #                    else sy_.getfilesystemencoding() # TODO: currently unused (check if needed to deal with QT widget encoding)
    cf_.PrintConfig(
        config, has_default_value, console=console, end_character=end_character
    )

    # --- CONFIGURATION -> PARAMETERS
    #
    alg_mpp_prm = config[std_label.sct_mpp]
    alg_ref_prm = config[std_label.sct_refinement]
    alg_fbk_prm = config[std_label.sct_feedback]

    mkt_bth_prm = config[std_label.sct_object]  # bth=birth
    mkt_rng_prm = config[std_label.sct_object_ranges]
    mkt_qty_prm = config[std_label.sct_quality]
    mkt_qpm_prm = config[std_label.sct_quality_prm]  # qpm=quality parameters
    mkt_cst_prm = config[std_label.sct_constraints]

    sig_ldg_prm = config[std_label.sct_signal]  # ldg=loading
    sig_lpm_prm = config[std_label.sct_signal_loading_prm]  # lpm=loading parameters
    sig_prg_prm = config[std_label.sct_signal_processing_prm]

    out_res_prm = config[std_label.sct_output]  # res=result
    out_dsp_prm = config[std_label.sct_output_prm]  # dsp=display

    # --- OBJECT CLASS LOADING
    #
    mkpt_t: marked_point_t = im_.ElementInModule(
        mkt_bth_prm["object_type"],
        mod_name=mkt_bth_prm["object_module"],
        category="marked_point",
    )
    mkpt_t._NormalizeMarkRanges(mkt_rng_prm)
    if std_label.sct_object_ranges in for_deferred_check:
        del for_deferred_check[std_label.sct_object_ranges]

    simlar_mkpt_mtd = "SimilarMarkedPoints"
    if (alg_ref_prm["age_for_refinement"] is not None) and (
        not hasattr(mkpt_t, simlar_mkpt_mtd)
    ):
        raise ValueError(
            f"{mkpt_t}: MPP refinement cannot be used: "
            f"Missing {simlar_mkpt_mtd} method"
        )

    mkpt_dim = mkpt_t.dim

    # --- OBJECT QUALITY and RAW DATA TRANSFORMATION LOADING
    #
    mkpt_quality_env: quality_env_t = im_.ElementInModule(
        mkt_qty_prm["object_quality"],
        mod_name=mkt_qty_prm["object_quality_module"],
        category="quality",
    )
    ch_.CheckPassedParameters(mkpt_quality_env.SignalFromRawSignal.__name__, ex_.FunctionInfos(mkpt_quality_env.SignalFromRawSignal), sig_prg_prm, 1)
    ch_.CheckPassedParameters(mkpt_quality_env.MKPTQuality.__name__, ex_.FunctionInfos(mkpt_quality_env.MKPTQuality), mkt_qpm_prm, 2)
    if std_label.sct_signal_processing_prm in for_deferred_check:
        del for_deferred_check[std_label.sct_signal_processing_prm]
    if std_label.sct_quality_prm in for_deferred_check:
        del for_deferred_check[std_label.sct_quality_prm]

    # --- RAW DATA READING PREPARATION
    #
    SignalLoading_fct: Callable = im_.ElementInModule(
        sig_ldg_prm["signal_loading_function"],
        mod_name=sig_ldg_prm["signal_loading_module"],
        elm_is_class=False,
    )
    ch_.CheckPassedParameters(SignalLoading_fct.__name__, ex_.FunctionInfos(SignalLoading_fct), sig_lpm_prm, 3)
    if std_label.sct_signal_loading_prm in for_deferred_check:
        del for_deferred_check[std_label.sct_signal_loading_prm]

    signal_base_path = pl_path_t(sig_ldg_prm["signal_path"])
    signal_path_is_folder = signal_base_path.is_dir()

    vmap_base_path = sig_ldg_prm["vmap_path"]
    if vmap_base_path is None:
        signal_has_vmap = vmap_path_is_folder = False
    else:
        vmap_base_path = pl_path_t(vmap_base_path)
        signal_has_vmap = True
        vmap_path_is_folder = vmap_base_path.is_dir()
        if vmap_path_is_folder:
            assert signal_path_is_folder, (
                f"{__name__}: validity map path cannot be a folder if signal path refers to a single datum\n"
                f"    Validity map path: {vmap_base_path}\n"
                f"    Signal path:       {signal_base_path}"
            )

    # --- DATA OUTPUT PREPARATION
    #
    if out_res_prm["result_output_function"] is None:
        SignalOutput_fct = lambda mkpt_lst_, center_rng_, raw_signal_, **kwargs: True
    else:
        SignalOutput_fct = im_.ElementInModule(
            out_res_prm["result_output_function"],
            mod_name=out_res_prm["result_output_module"],
            elm_is_class=False,
        )
        ch_.CheckPassedParameters(SignalOutput_fct.__name__, ex_.FunctionInfos(SignalOutput_fct), out_dsp_prm, 3)
        if std_label.sct_output_prm in for_deferred_check:
            del for_deferred_check[std_label.sct_output_prm]

    output_folder = out_res_prm["output_path"]

    # --- DETECTION PROCEDURE
    #
    from brick.marked_point.signal_context import signal_context_t
    import imageio as io_

    assert for_deferred_check == {}

    if isinstance(mkt_bth_prm["center_rng"], pl_path_t):
        _, mkt_bth_prm["center_rng"] = SignalLoading_fct(
            mkt_bth_prm["center_rng"], requested_dim=mkpt_dim
        )
    elif isinstance(mkt_bth_prm["center_rng"], tuple):
        center_rng_len = mkt_bth_prm["center_rng"].__len__()
        assert (
            center_rng_len // 2 == mkpt_dim
        ), f"center_rng: Must have length {2*mkpt_dim} or {2*mkpt_dim+1}; Actual={center_rng_len}"

    if signal_path_is_folder:
        raw_signal_lst = signal_base_path.glob(
            "*.*"
        )  # TODO: see if interesting to replace with rglob (will require hierarchy mirroring between signal and vmap)
    else:
        raw_signal_lst = (signal_base_path,)

    validity_map = None

    marked_points = {}
    for signal_idx, signal_path in enumerate(raw_signal_lst, start=1):
        print(f"Signal.{signal_idx}: {signal_path}", end=end_character, file=console)
        signal_id = f"{signal_path.stem}_{signal_path.suffix[1:]}"

        # --- --- DATA READING and PREPARATION
        #
        try:
            if signal_has_vmap and (vmap_path_is_folder or (validity_map is None)):
                if vmap_path_is_folder:
                    vmap_path = vmap_base_path / signal_path.relative_to(signal_base_path)
                else:
                    vmap_path = vmap_base_path
                signal_size, raw_signal, validity_map = SignalLoading_fct(
                    signal_path,
                    vmap_path=vmap_path,
                    requested_dim=mkpt_dim,
                    **sig_lpm_prm,
                )
            else:
                signal_size, raw_signal = SignalLoading_fct(
                    signal_path, requested_dim=mkpt_dim, **sig_lpm_prm
                )
        except Exception as exc:
            print(
                f"---\nUnable to load signal and/or signal validity map\n{exc}\nIgnoring\n---",
                end=end_character,
                file=console,
            )
            continue
        # If signal_path_is_folder, raw signal need not have the same shape, unless mkt_bth_prm['center_rng'] is an array_t.
        # In this latter case, shape compatibility is checked in CreateCenterGenerator.

        signal_for_qty = mkpt_quality_env.SignalFromRawSignal(
            raw_signal, vmap=validity_map, **sig_prg_prm
        )
        MKPTQuality_fct = lambda mkpt_: mkpt_quality_env.MKPTQuality(
            mkpt_, signal_for_qty, **mkt_qpm_prm
        )
        signal_context_t.CreateFrom(
            signal_size, raw_signal, signal_for_qty, validity_map
        )

        # --- --- MPP-BASED OBJECT DETECTION
        #
        higher_from_tos = tuple(
            item
            for sublist in zip(
                (mkpt_dim - 1) * (0,), (size - 1 for size in signal_size[1:])
            )
            for item in sublist
        )  # higher=for dimensions higher than the first one

        if (alg_mpp_prm["n_parallel_workers"] != 1) and (
            pl_.get_start_method(allow_none=False) == "fork"
        ):
            if alg_mpp_prm["n_parallel_workers"] > 0:
                n_chunks = alg_mpp_prm["n_parallel_workers"]
            else:
                n_chunks = (3 * pl_.cpu_count()) // 2
        else:
            # Disables parallel computation if requested or if using Windows, since pickle cannot handle it
            n_chunks = 1

        alg_mpp_prm["n_births_per_iteration"] //= n_chunks
        sampler = mkpt_t.Sampler()
        sampler.__class__.Initialize(seed=alg_mpp_prm["seed"])
        sampler.SetMarkParameters(mkt_rng_prm, mkpt_t.marks_details)
        detection_prms = (
            mkt_bth_prm,
            mkt_cst_prm,
            mkt_qty_prm,
            alg_mpp_prm,
            alg_ref_prm,
            alg_fbk_prm,
            mkpt_t,
            sampler,
            MKPTQuality_fct,
            higher_from_tos,
        )

        if n_chunks > 1:
            # For the first dimension
            chunk_size = signal_size[0] // n_chunks
            remainder = signal_size[0] % n_chunks
            chunk_sizes = n_chunks * [chunk_size]
            for chunk_idx in range(remainder):
                chunk_sizes[chunk_idx] += 1

            from_tos = [(0, chunk_sizes[0] - 1)]
            for chunk_idx, chunk_size in enumerate(chunk_sizes[1:]):
                last_to = from_tos[chunk_idx][1]
                from_tos.append((last_to + 1, last_to + chunk_size))
            from_tos = tuple(from_tos)

            queue = pl_.Queue()
            processes = tuple(
                pl_.Process(
                    target=PartialDetection,
                    args=(*detection_prms, from_to, console, pid, queue),
                )
                for pid, from_to in enumerate(from_tos, start=1)
            )

            print(
                f"Processe(s): {processes.__len__()} with chunks {from_tos}",
                end=end_character,
                file=console,
            )

            for process in processes:
                process.start()

            overlap_tolerance = mkt_cst_prm["overlap_tolerance"]
            mkpt_lst = []
            # From: https://stackoverflow.com/questions/31708646/process-join-and-queue-dont-work-with-large-numbers
            # Answer by: Patrick Maupin (answered Jul 29 '15 at 19:59, edited Dec 8 '15 at 23:45)
            while True:
                running = any(process.is_alive() for process in processes)
                while not queue.empty():
                    partial_lst = queue.get()
                    partial_lst = list(
                        map(lambda info: RebuiltMKPT(info, mkpt_t), partial_lst)
                    )
                    mp_.UpdateDetectedSoFar(mkpt_lst, partial_lst, overlap_tolerance)
                if not running:
                    break
            # Alternative (by same author):
            # liveprocs = list(processes)
            # while liveprocs:
            #     try:
            #         while 1:
            #             process_queue_data(q.get(False))
            #     except Queue.Empty:
            #         pass
            #
            #     time.sleep(0.5)    # Give tasks a chance to put more data in
            #     if not q.empty():
            #         continue
            #     liveprocs = [p for p in liveprocs if p.is_alive()]

            for process in processes:
                process.join()
        else:
            mkpt_lst = PartialDetection(
                *detection_prms, (0, signal_size[0] - 1), console
            )
        signal_context_t.Clear()
        mkpt_lst.sort(key=lambda mkpt_: mkpt_.quality, reverse=True)

        # --- --- DETECTION OUTPUT
        #
        if mkpt_lst.__len__() > 0:
            marked_points[signal_path.__str__()] = tuple(mkpt_lst)
            import matplotlib.pyplot as plt_
            import numpy as np_
            from pathlib import Path
            ni = 0           
            output_path_localmap = output_folder / f"local_map_{signal_id}_{start_as_str}"
            Path(output_path_localmap).mkdir(parents=True, exist_ok=True)

            for mkpt in mkpt_lst:
                ellipse_map = np_.full(signal_context_t.dom_size, 2.0)
                ni+=1
                #local_map = np_.full(signal_context_t.dom_size, 2.0)[mkpt.bbox.domain]
                local_map = ellipse_map[mkpt.bbox.domain]
                local_map[:,:] = np_.sqrt(mkpt.SqOneDistanceMap())
                local_map[local_map > 1.0] = 2.0
                localmap_fullname = output_path_localmap / f"local_map_{ni}"
                #localmap_fullname = output_folder / f"localmap_{signal_id}" / _OutputDocName(
                #    f"localmap_{ni}", "png", start_as_str, signal_id)
                io_.imwrite(f"{localmap_fullname}.png", (ellipse_map*255).astype(np_.uint8))
                np_.save(localmap_fullname, ellipse_map)
                
        else:
            print("No MPs detected", end=end_character, file=console)
            continue

        import brick.marked_point.mkpt_list as ml_
        import tempfile as tp_

        if not output_folder.exists():
            try:
                output_folder.mkdir()
            except Exception as exc:
                print(
                    f"{output_folder}: folder creation failed\n({exc})",
                    end=end_character,
                    file=console,
                )
                output_folder = pl_path_t(tp_.mkdtemp())
                print(
                    f"{output_folder}: temporary alternative output folder",
                    end=end_character,
                    file=console,
                )

        cf_.WriteConfigToIniDocument(
            config,
            output_folder / _OutputDocName("config", "ini", start_as_str, signal_id),
        )

        if out_res_prm["console"]:
            print(f"MP(s) @ {start_as_str}", end=end_character, file=console)
            if console == sy_.stdout:
                for mkpt in mkpt_lst:
                    print(mkpt, end=end_character, file=console)
            else:  # Any object that has a "write" method (typically, a widget of a GI)
                ml_.PrintMarkedPointListInCSVStyle(
                    mkpt_lst, console=console, end_character=end_character
                )

        if out_res_prm["marks_output"]:
            csv_fullname = output_folder / _OutputDocName(
                "marks", "csv", start_as_str, signal_id
            )
            with open(
                csv_fullname, "w", encoding=sy_.getfilesystemencoding()
            ) as csv_accessor:
                ml_.WriteMarkedPointsToCSV(
                    mkpt_lst, mkpt_quality_env, csv_accessor
                )

        if out_res_prm["contour_output"]:
            contour_map = ml_.MarkedPointListContourMap(mkpt_lst)
            if mkpt_dim == 2:
                contour_fullname = output_folder / _OutputDocName(
                    "contour", "png", start_as_str, signal_id
                )
                io_.imwrite(contour_fullname, contour_map)
            elif mkpt_dim == 3:
                contour_fullname = output_folder / _OutputDocName(
                    "contour", "tif", start_as_str, signal_id
                )
                io_.volwrite(contour_fullname, contour_map)
            else:
                print(
                    f"Contour output in {mkpt_dim}-D not implemented",
                    end=end_character,
                    file=console,
                )

        if out_res_prm["region_output"]:
            region_map = ml_.MarkedPointListRegionMap(mkpt_lst)
            if mkpt_dim == 2:
                region_fullname = output_folder / _OutputDocName(
                    "region", "png", start_as_str, signal_id
                )
                io_.imwrite(region_fullname, region_map)
            elif mkpt_dim == 3:
                region_fullname = output_folder / _OutputDocName(
                    "region", "tif", start_as_str, signal_id
                )
                io_.volwrite(region_fullname, region_map)
            else:
                print(
                    f"Region output in {mkpt_dim}-D not implemented",
                    end=end_character,
                    file=console,
                )

        # Leave here so that in case it contains blocking instructions (like matplotlib show()),
        # it does not delay saving to files above.
        SignalOutput_fct(
            mkpt_lst,
            mkt_bth_prm["center_rng"],
            raw_signal,
            result_folder=output_folder,
            signal_id=signal_id,
            date_as_str=start_as_str,
            **out_dsp_prm,
        )

    return marked_points


def PartialDetection(
    mkt_bth_prm,
    mkt_cst_prm,
    mkt_qty_prm,
    alg_mpp_prm,
    alg_ref_prm,
    alg_fbk_prm,
    mkpt_t,
    sampler,
    MKPTQuality_fct,
    higher_from_tos,
    from_to: tuple,
    console=None,
    pid: int = 1,
    queue: Optional[pl_.Queue] = None,
) -> Optional[list]:
    #
    if mkt_bth_prm["center_rng"] is None:
        local_center_rng = (*from_to, *higher_from_tos)
    elif isinstance(mkt_bth_prm["center_rng"], tuple):
        local_center_rng = (
            max(from_to[0], mkt_bth_prm["center_rng"][0]),
            min(from_to[1], mkt_bth_prm["center_rng"][1]),
            *mkt_bth_prm["center_rng"][2:],
        )
        if local_center_rng[0] > local_center_rng[1]:
            return
    else:  # isinstance(mkt_bth_prm['center_rng'], array_t)
        # TODO: the code below is valid for 2-D only
        local_center_rng = mkt_bth_prm["center_rng"].copy()
        local_center_rng[: from_to[0], :] = 0
        local_center_rng[(from_to[1] + 1) :, :] = 0
        if (local_center_rng == 0).all():
            return
    sampler.SetPointParameters(local_center_rng)

    mkpt_lst = mp_.DetectedObjects(
        mkpt_t,
        MKPTQuality_fct,
        sampler,
        n_iterations=alg_mpp_prm["n_iterations"],
        n_births_per_iteration=alg_mpp_prm["n_births_per_iteration"],
        only_uncropped=mkt_bth_prm["only_uncropped"],
        age_for_refinement=alg_ref_prm["age_for_refinement"],
        n_refinement_attempts=alg_ref_prm["n_refinement_attempts"],
        refinement_fraction=alg_ref_prm["refinement_fraction"],
        min_quality=mkt_qty_prm["min_quality"],
        overlap_tolerance=mkt_cst_prm["overlap_tolerance"],
        status_period=alg_fbk_prm["status_period"],
        console=console,
        pid=pid,
        queue=queue,
    )

    if queue is None:
        return mkpt_lst


def RebuiltMKPT(info: tuple, mkpt_t) -> Any:
    #
    mkpt = mkpt_t(*info[:-2], check_marks=False)
    mkpt.quality = info[-2]
    mkpt.age = info[-1]

    return mkpt


def _OutputDocName(
    basename: str, extension: str, date_as_str: str, signal_id: str
) -> str:
    #
    return f"{signal_id}-{basename}-{date_as_str}.{extension}"


if __name__ == "__main__":
    #
    parser = cf_.CommandLineParser()
    args = parser.parse_args()

    if args.ini_document is None:
        ini_document_ = None
        config_ = cf_.DefaultConfig()
    else:
        ini_document_ = pl_path_t(args.ini_document)
        if not ini_document_.is_file():
            raise FileNotFoundError(f"{ini_document_}: file not found")
        config_ = cf_.TypedConfig(ini_document_)

    cf_.OverwriteConfigWithArgs(config_, args)
    config_is_valid, for_deferred_check_ = an_.ConfigIsValid(config_)
    if not config_is_valid:
        parser.print_usage()
        sy_.exit(-1)

    _ = RunDetector(config_, for_deferred_check_, ini_document_)
