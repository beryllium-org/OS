rename_process("advance build date")
systemprints(2, "Advancing time to build date")
if time.localtime()[0] < 2021:
    be.based.run(
        "date",
        [
            "set",
            str(be.api.getvar("IMPLEMENTATION_DATE").split("-"))[1:-1]
            .replace("'", "")
            .replace(",", ""),
        ],
    )
    systemprints(1, "Advancing time to build date")  # Ok
else:
    systemprints(5, "Advancing time to build date")  # Skipped
