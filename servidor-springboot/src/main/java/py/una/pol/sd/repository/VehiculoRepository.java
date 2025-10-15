package py.una.pol.sd.repository;

import java.util.List;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;
import py.una.pol.sd.model.Vehiculo;

@Repository
public interface VehiculoRepository extends CrudRepository<Vehiculo, Long> {
    List<Vehiculo> findAll();

}
