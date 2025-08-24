from controller.databricks_controller import DatabricksController
from view.databricks_views import ConsoleView

if __name__ == "__main__":
    controller = DatabricksController()
    table_name = "workspace.default.validation_totvs"
    df = controller.get_table_data(table_name)

    view = ConsoleView()
    view.display_table(df)








