package py.una.pol.sd.repository;

import java.util.List;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import py.una.pol.sd.model.Viaje;


@Repository
public interface ViajeRepository extends CrudRepository<Viaje, Long> {
    List<Viaje> findAll();
}