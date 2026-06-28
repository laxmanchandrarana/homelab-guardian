class DiagnosisRules:

    RULES = [

        {
            "pattern": "oomkilled",
            "cause": "OUT_OF_MEMORY",
            "confidence": 0.99,
        },

        {
            "pattern": "no space left",
            "cause": "DISK_FULL",
            "confidence": 0.98,
        },

        {
            "pattern": "permission denied",
            "cause": "PERMISSION",
            "confidence": 0.96,
        },

        {
            "pattern": "connection refused",
            "cause": "DATABASE_DOWN",
            "confidence": 0.94,
        },

        {
            "pattern": "failed to connect",
            "cause": "NETWORK",
            "confidence": 0.90,
        },

        {
            "pattern": "unhealthy",
            "cause": "HEALTHCHECK",
            "confidence": 0.93,
        },

        {
            "pattern": "segmentation fault",
            "cause": "CRASH",
            "confidence": 0.99,
        },

        {
            "pattern": "panic",
            "cause": "CRASH",
            "confidence": 0.95,
        },

        {
            "pattern": "python 3 is missing",
            "cause": "DEPENDENCY",
            "confidence": 0.88,
        },

        {
            "pattern": "received sigterm",
            "cause": "MANUAL_STOP",
            "confidence": 0.80,
        }

    ]
