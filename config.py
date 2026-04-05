import structlog


structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="%H:%M:%S"),
        structlog.dev.ConsoleRenderer(
            colors=True,
            level_styles={
                "debug": "\x1b[40m\x1b[37m",
                "info": "\x1b[44m\x1b[97m\x1b[1m",
                "warning": "\x1b[43m\x1b[30m",
                "error": "\x1b[41m\x1b[97m\x1b[1m",
                "critical": "\x1b[45m\x1b[97m\x1b[1m",
            },
        ),
    ]
)

logger = structlog.get_logger()
