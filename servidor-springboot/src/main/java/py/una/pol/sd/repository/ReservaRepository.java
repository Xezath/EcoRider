package py.una.pol.sd.repository;

import java.util.List;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;
import py.una.pol.sd.model.Reserva;

@Repository
public interface ReservaRepository extends CrudRepository<Reserva, Long> {
    List<Reserva> findAll();
}
