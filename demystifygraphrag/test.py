from kedro.framework.session import KedroSession
from kedro.framework.project import configure_project

package_name = "demystifygraphrag"
configure_project(package_name)

with KedroSession.create(package_name) as session:
    session.run()