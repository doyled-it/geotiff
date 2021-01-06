from tifffile.tifffile_geodb import Proj, GCSE, PCS, GCS, Ellipse, DatumE, Datum  # type: ignore
from typing import List, Tuple
from difflib import SequenceMatcher
from .geotiff_logging import log

PreDict = List[Tuple[str, int]]


def crs_code_gusser(GTCitationGeo: str) -> Tuple[int, int]:
    """This is a very hacky solution to the problem of finding the correct 
    crs code based on the GTCitationGeoKey string.

    Args:
        GTCitationGeo (str): GT Citation Geo Key

    Returns:
        Tuple[int, int]: ([The crs code], [the score of the guess from 0 to 1])
    """
    log.warning(
        "Making a guess for the crs_code based on the GTCitationGeoKey. Could be incorrect!")
    crs_code: int = 32767
    projs: PreDict = [(name, member.value)
                      for name, member in Proj.__members__.items()]
    pcss: PreDict = [(name, member.value)
                     for name, member in PCS.__members__.items()]
    gcse: PreDict = [(name, member.value)
                     for name, member in GCSE.__members__.items()]
    gcs: PreDict = [(name, member.value)
                    for name, member in GCS.__members__.items()]
    # ! handel these!
    ellipse: PreDict = [(name, member.value)
                        for name, member in Ellipse.__members__.items()]
    datumE: PreDict = [(name, member.value)
                       for name, member in DatumE.__members__.items()]
    datum: PreDict = [(name, member.value)
                      for name, member in Datum.__members__.items()]
    all_crs = dict(projs + pcss + gcse + gcs)  # + ellipse + datumE + datum)
    # takes a guess based on the GTCitationGeoKey
    info_str: str = GTCitationGeo
    best_score: float = 0.0
    crs_key: str = ""
    for crs in all_crs.keys():
        score: float = SequenceMatcher(None, info_str, str(crs)).ratio()
        if score > best_score:
            best_score = score
            crs_key = crs
            crs_code = all_crs[crs_key]

    return(crs_code, best_score)
