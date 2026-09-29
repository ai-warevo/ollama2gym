"""Module for the Tic-Tac-Toe GUI implementation."""

import dearpygui.dearpygui as dpg  # type: ignore

from core.logger import get_logger

from .engine import TicTacToeEngine

logger = get_logger("tictactoe.gui")


class TicTacToeGUI:
    """
    A modern GUI for TicTacToeEngine implemented using Dear PyGui.
    Replaces Tkinter to avoid system-level TK dependencies.
    """

    # Color Constants (RGBA)
    COLOR_BG = (26, 26, 26, 255)  # #1A1A1A
    COLOR_X = (0, 229, 255, 255)  # #00E5FF (Neon Blue)
    COLOR_O = (255, 61, 0, 255)  # #FF3D00 (Neon Orange/Red)
    COLOR_TEXT = (255, 255, 255, 255)  # #FFFFFF
    COLOR_BTN_NORMAL = (38, 38, 38, 255)

    def __init__(self, engine: TicTacToeEngine) -> None:
        logger.debug("Initializing GUI")
        self.engine = engine
        self._setup_dpg()
        self._create_ui()
        self._apply_global_theme()
        # Pre-create and bind themes for X and O to avoid overhead during gameplay
        self._prepare_item_themes()

    def _setup_dpg(self) -> None:
        """Initializes the Dear PyGui context and viewport."""
        logger.debug("Setting up DPG")
        dpg.create_context()
        dpg.create_viewport(title="Tic-Tac-Toe Pro", width=400, height=520)

    def _create_ui(self) -> None:
        """Builds the UI layout."""
        logger.debug("Creating UI")
        with dpg.window(label="Game Window", tag="PrimaryWindow"):
            dpg.add_text("TIC TAC TOE", color=list(self.COLOR_TEXT))
            dpg.add_spacer(height=20)

            # Grid Construction
            for row in range(3):
                with dpg.group(horizontal=True):
                    for col in range(3):
                        idx = row * 3 + col
                        dpg.add_button(
                            label="",
                            width=100,
                            height=80,
                            tag=f"btn_{idx}",
                            callback=self._on_click,
                            user_data=idx,
                        )
                        if col < 2:
                            dpg.add_spacer(width=10)  # Space between columns
                    dpg.add_spacer(height=10)  # Space between rows

            dpg.add_spacer(height=30)

            # Status Label
            self.status_tag = "StatusLabel"
            dpg.add_text("", tag=self.status_tag, color=list(self.COLOR_TEXT))

            dpg.add_spacer(height=20)

            # Restart Button
            dpg.add_button(
                label="RESTART GAME", width=150, height=40, callback=self._on_restart
            )

    def _apply_global_theme(self) -> None:
        """Applies the dark theme."""
        with dpg.theme() as global_theme, dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, list(self.COLOR_BG))
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, list(self.COLOR_BG))
            dpg.add_theme_color(dpg.mvThemeCol_Button, list(self.COLOR_BTN_NORMAL))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (51, 51, 51, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (0, 0, 0, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Text, list(self.COLOR_TEXT))

        dpg.bind_theme(global_theme)
        dpg.configure_item("PrimaryWindow", no_title_bar=True)

    def _prepare_item_themes(self) -> None:
        """Creates specific themes for X and O to control text color."""
        # Theme for X (Neon Blue Text)
        with dpg.theme() as self.theme_x, dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Text, list(self.COLOR_X))

        # Theme for O (Neon Red Text)
        with dpg.theme() as self.theme_o, dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Text, list(self.COLOR_O))

        # Default theme for buttons (Normal Text Color)
        with dpg.theme() as self.theme_default, dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Text, list(self.COLOR_TEXT))

    def _on_click(self, _sender: int, _app_data: int, user_data: int) -> None:
        logger.debug("Button clicked: %s", user_data)
        if self.engine.make_move(user_data):
            self._update_display()
        else:
            logger.warning("Invalid click at position %s", user_data)

    def _on_restart(self) -> None:
        logger.info("Restart requested")
        self.engine.reset()
        self._update_display()

    def _update_display(self) -> None:
        board = self.engine.get_board()
        winner = self.engine.get_winner()
        is_draw = self.engine.is_draw
        current_player = self.engine.get_current_player()

        # Update Buttons logic
        for i in range(9):
            val = board[i]
            btn_tag = f"btn_{i}"
            if val == TicTacToeEngine.PLAYER_X:
                dpg.configure_item(btn_tag, label="X")
                dpg.bind_item_theme(btn_tag, self.theme_x)
            elif val == TicTacToeEngine.PLAYER_O:
                dpg.configure_item(btn_tag, label="O")
                dpg.bind_item_theme(btn_tag, self.theme_o)
            else:
                dpg.configure_item(btn_tag, label="")
                dpg.bind_item_theme(btn_tag, self.theme_default)

        # Update Status Text
        status_text = ""
        status_color = list(self.COLOR_TEXT)

        if winner == TicTacToeEngine.PLAYER_X:
            status_text = "PLAYER X WINS!"
            status_color = list(self.COLOR_X)
        elif winner == TicTacToeEngine.PLAYER_O:
            status_text = "PLAYER O WINS!"
            status_color = list(self.COLOR_O)
        elif is_draw:
            status_text = "IT'S A DRAW!"
            status_color = list(self.COLOR_TEXT)
        else:
            player_name = "X" if current_player == TicTacToeEngine.PLAYER_X else "O"
            status_text = f"TURN: PLAYER {player_name}"

        dpg.set_value(self.status_tag, status_text)
        dpg.configure_item(self.status_tag, color=status_color)

    def run(self) -> None:
        """Starts the Dear PyGui loop."""
        logger.info("Starting GUI loop")
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

    def info(self) -> None:
        """Dummy public method to satisfy pylint."""
