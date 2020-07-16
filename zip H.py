import zipfile as zf
import logging

logging.basicConfig(level=logging.INFO)
logging.info("Creating a variable with %s bytes..." % zf.ZIP64_LIMIT)
hs = b"H" * zf.ZIP64_LIMIT
maxFiles = zf.ZIP_FILECOUNT_LIMIT
logging.info("Creating zip file...")
with zf.ZipFile("H.zip", "a", compression=zf.ZIP_LZMA, compresslevel=9) as z:
    for i in range(maxFiles):
        logging.info("Writing file no. {}/{} inside of zip file...".format(i + 1, maxFiles))
        with z.open("H {}.txt".format(i), "w") as f:
            f.write(hs)
logging.info("Finished")
